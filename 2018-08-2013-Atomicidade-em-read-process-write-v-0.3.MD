# Simular comportamento atômico em operações de microsserviços que dependam de recursos externos que não suportam transações distribuídas.

Data: 2018-08-13

## Status
Proposto

## Contexto
Nas aplicações compostas por microsserviços é desejável ter atomicidade local das operações expostas pela API, sendo então que para o mundo externo essas operações são concluídas com sucesso ou não são executadas pelos microsserviços e efeitos colaterais e/ou mudanças de estado não são ocasionados.

O sistema o qual estamos projetando é composto por vários microsserviços, sendo uma categoria de fluxo de processamento bastante comum a descrita a seguir:
1)	Consumir uma mensagem A de um tópico-partição Kafka tpX
2)	Gravar os dados resultantes do processamento/transformação da mensagem A em uma base de dados, como por exemplo Cassandra
3)	Produzir uma mensagem B no tópico-partição Kafka tpy
4)	Marcar a mensagem A como consumida (comitar offset do tópico tpX).

Esse tipo de operação é conhecido como read-process-write.

Falhas tanto nos sistemas de apoio, Kafka e Cassandra, quanto nos microsserviços da aplicação podem ocasionar que operações sejam executadas de maneira errada e/ou que o estado de alguma entidade fique inconsistente/errôneo na base de dados. Podemos exemplicar algumas situações:

1)	Uma mensagem A é consumida e ocorre uma falha no microsserviço durante o processamento da A, resultando que A foi marcada como processada mas de fato se perdeu.
2)	Uma mensagem A é consumida, processada, gravada no Cassandra e uma nova mensagem B produzida para outro tópico, porém a gravação no Cassandra não foi bem sucedida e não resultou em um erro no microsserviço
3)	Uma mensagem A é consumida, processada, gravada no Cassandra mas a aplicação quebra antes de produzir a mensagem B para o tópico de saída, resultando em um estado inconsistente na base de dados.
4)	Uma mensagem A é consumida, processada, gravada no Cassandra, uma mensagem B é produzida para o tópico de saída, porém a mensagem A não pode ser marcada como consumida e será reprocessada, podendo resultar em inconsistências.

Fica evidente que para um fluxo de read-process-write ser bem sucedido é necessário que uma mensagem A somente seja marcada como consumida se o processamento, incluso escrita em base de dados, e a produção da mensagem B de resultado sejam bem sucedidos e que também o fluxo seja revertido em qualquer caso de falha, inclusive quando não é possível marcar a mensagem como consumida.

## Decisão
O  uso de Apache Kafka nos fornece algumas garantias, como por exemplo contexto transacional em fluxos de read-process-write e processamento de mensagens exaclty-once, ou seja, não há envio duplicado de mensagens, nem consumo duplicado de mensagens e é possível consumir uma mensagem A e produzir uma mensagem B de maneira atômica com contexto transacional, utilizando a configuração enable.idempotence=true no produtor e isolation.level=read_committed no consumidor, conforme detalhado nos seguintes artigos:

https://www.confluent.io/blog/transactions-apache-kafka/

https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/

Então é necessário verificar como lidar com falhas e estado de dados inconsistente na base de dados Cassandra, logo vamos considerar o seguinte cenário:

[logo]: read-process-write.png "Read-process-write com Kafka e Cassandra"
![alt-tex][logo]
<center>
    <i>
        Ilustração de Read-process-write com Kafka e Cassandra<br/>
        <sub>
            (O processo acima é apenas um exemplo e pode não refletir a realidade.)
        </sub>
    </i>
</center>
<br/>

```java {.line-numbers}
producer.initTransactions();
try {

	//puxando mensagens do consumidor
	ConsumerRecords recordToConsume = consumer.poll();

	//iniciando transação Kafka;
  producer.beginTransaction();

	//Processando mensagens consumidas
  DataObject data  = process(record);
	ProducerRecord<> recordToProduce = generateMessage("target-topic", data);

	//Enviando novas mensagens para o tópico de saída e adicionando o offset do tópico consumido para a transação
	producer.send(recordToProduce);
	producer.sendOffsetsToTransaction(currentOffsets(consumer), group);

	//Escrevendo dados no Cassandra
	cassandraRepo.write(data);

	//finalizando a transação
  producer.commitTransaction();
 } catch (ProducerFencedException | OutOfOrderSequenceException | AuthorizationException e) {
    // Tratamento de exceções não recuperáveis, a única opção é fechar a conexão do produtor
    producer.close();
 } catch (KafkaException kafkaException | RequestExecutionException cassandraRequestException) {
    // Para outras exceções do Kafka e Cassandra, abortar a transação.
  producer.abortTransaction();
 } catch (DriverException cassandraDriverException) {
	// Exceções de driver não executam requisições ao Cassandra
	producer.abortTransaction();
 }
```

Erros ocorridos entre e incluído os passos 1 ao 5 são tratados abortando a transação, pois nenhum efeito colateral ou escrita de dados foi efetuada até o momento, logo ao abortar a transação a mensagem A não terá seu offset atualizado e será reconsumida futuramente. No código de exemplo acima essa operação é exemplificada pelo tratamento da exceção KafkaException.

####Fluxo de exceção com efeito colateral: Erro no passo 6

Quando o ocorre um erro de escrita no Cassandra, como um WriteTimeoutException, não é possível saber com certeza se o dados foram ou não persistidos na base de dados.

Logo é necessário efetuar uma retentativa da escrita na base de dados e essa retentativa pode ser efetuada em dois passos distintos:

######Configuração de retentativa automática na biblioteca driver do Cassandra.
Podemos configurar uma política de rentativa na conexão da aplicação do Cassandra, de modo que a operação será retentada um número de vezes de acordo com a política de maneira transparente antes de levantar uma exceção para a aplicação. Ao utilizar operações idempotentes a retentativa é segura e não vai gerar dados duplicados na base de dados.

A configuração de retentativas do Cassandra é feita na aplicação no momento de instanciar a conexão com o cluster Cassandra, como exemplificado abaixo:

```java {.line-numbers}
Cluster cluster = Cluster.builder()
        .addContactPoint("127.0.0.1")
        .withRetryPolicy(DefaultRetryPolicy)
        .build();
```        

O Cassandra disponibiliza algumas políticas de retentativa e é possível também criar uma política customizada implementando a interface RetryPolicy. Caso nenhuma política seja explicitamente configurada é utilizada por padrão DefaultRetryPolicy, a qual tem o comportamento de só efetuar uma única retentativa e somente para operações do tipo WriteType.BATCH_LOG. A política padrão é recomendada pois tem uma abordagem de somente retentar operações de escrita que garantam o mesmo nível de consistência da operação.

Seguem documentos com mais detalhes sobre o mecanismo de retentativas:

https://datastax.github.io/python-driver/api/cassandra/policies.html
https://docs.datastax.com/en/developer/java-driver/3.4/manual/retries/   

######Abortar transação Kafka e reprocessar mensagem.
Caso as retentativas automáticas falhem devemos abortar a transação Kafka, o que resultará que a mensagem seja consumida novamente em outro momento. Como estamos trabalhando com o contexto de operações idempotentes logo o reprocessamento da mensagem não vai resultar em operação duplicada de escrita no Cassandra caso os dados tenham sido persistidos apesar da falha na base de dados.

Vale notar também que caso os dados tenham sido persistidos de fato na base e que a transação tenha sido abortada, outras operações do microsserviço podem ser impactadas, como consultas por exemplo, ou operações que dependam da mensagem que deveria ter sido produzida pelo microsserviço, já que os dados estarão na base enquanto a mensagem original esta sendo reprocessada.

Seguem artigos e documentações que explicam melhor idempotência e tratamento de erros no Cassandra:

https://www.datastax.com/dev/blog/cassandra-error-handling-done-right
https://docs.datastax.com/en/cql/3.3/cql/cql_using/useInsertLWT.html

####Fluxo de exceção com efeito colateral: Erro no passo 7
Quando a falha acontece após a escrita no Cassandra a tratativa é abortar a transação e reprocessar a mensagem, similar ao caso descrito acima onde todas as retentativas automáticas de escrita falharam.

Nesse caso hávera dados persistidos na base cujas mensagens originais serão reprocessadas, podendo impactar outras operações do microsserviço como foi explicado na tratamento de falhas no passo 6.

## Consequências

As tratativas acima consideram casos de operações idempotentes, o que nem sempre é o caso. Há estruturas de dados, como counter columns e dados de tipo lista, que não suportam operações idempotentes, sendo que sendo esse caso é necessário ter um tratamento diferenciado ao ocorrer erros de escrita no Cassandra e que deve ser avalidado caso a caso.

Vale ressaltar que mesmo considerando a utilização de operações idempotentes os cenários de erros nos passos 6 e 7 podem ocasionar que dados estejam persistidos no Cassandra, e disponíveis para consulta, enquanto as mensagens referentes aquele dados estão sendo reconsumidas, o que pode impactar em outras funcionalidades do sistema, sendo que no momento não vemos uma forma melhor de tratar essa situação.

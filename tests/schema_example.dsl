namespace com.itau.checkAccount:
	enum StatusPessoa:
		aprovado
		reprovado 

	alias id long
	alias nome string(256)
	alias dinheiro decimal(19,4) >
			Tipo decimal, com precisão de 19 e 4 casas decimais para representar 
			valores monetários
	alias codigoPessoa id "código identificador de uma pessoa cliente do banco."
	alias codigoInstituicao id "codigo da instituição bancária"

	record PessoaCurto
		"Identifica a pessoa apenas com o nome e código":
		CodigoPessoa codigoPessoa  "código da pessoa cliente do banco"
		NomePessoa nome? > 
			Nome completo da pessoa cliente do banco. 
			Em algumas situações será nulo.

	record StatusPessoa(PessoaCurto)
		"qual o status de uma pessoa no banco":
		Status StatusPessoa

	record Conta "informacoes sobre uma conta":
		CodigoInstituicao codigoInstituicao 
		CodigoAgencia id 
		CodigoConta id 
		DAC int "digito verificador do codico de conta"

	record TEF "representação da transferência eletronica de fundos":
		CodigoTEF long  "codigo de identificação único da TEF"
		JWTCliente text?  "token JWT enviado pelo dispositivo do cliente"
		Solicitante PessoaCurto  "identificação da conta solicitante da TEF"
		CodigoCanal text  "identificação do código do canal pelo qual a TEF foi solicitada"
		ContaOrigem Conta  "Conta origem da solicitação que será debitada"
		CotaDestino Conta  "Conta destino da solicitação que será creditada"
		Valor Dinheiro  "Valor sendo transferido"
		LiteralExtrato string?(9)
		Comentario string?(256) "comentário associado à TEF feito pelo cliente da conta origem"
		DataSolicitação timestamp  "data e hora que o serviço de TEF recebeu a solicitação"
		DataEfetivacao timestamp? "data e hora que a TEF foi efetuada"

	record TEFValidada "indica que o quando a solicitação da TEF está validada":
		TEFValidada TEF 
		EhValida boolean
			

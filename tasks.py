from invoke import task

@task
def uml_model(c):
    c.run("plantuml ./docs/scheman_model.uml")


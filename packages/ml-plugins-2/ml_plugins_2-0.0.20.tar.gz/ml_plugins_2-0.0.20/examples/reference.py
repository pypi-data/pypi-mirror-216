from metaflow import step, batch, retry, get_metadata
from metaflow.flowspec import FlowSpec
from metaflow.includefile import IncludeFile
from plugins.poetry.plugin import poetry
from plugins.pip.plugin import pip, extra

class PluginFlow(FlowSpec):

    pyproject =  IncludeFile('names', default="pyproject.toml")
    lockfile = IncludeFile('do_not', default="poetry.lock")
    requirements = IncludeFile('matter', default="requirements.txt")

    @step
    def start(self):
        """
        The 'start' step is a regular step, so runs locally on the machine from
        which the flow is executed.
        """

        print("HelloAWS is starting.\n")
        print("Using metadata provider: %s\n" % get_metadata())
        print("The start step is running locally. Next, the ")
        print("'hello' step will run remotely on AWS batch. ")
        print("If you are running in the Netflix sandbox, ")
        print("it may take some time to acquire a compute resource.")

        self.next(self.hello)


    @batch(cpu=1, memory=500)
    @retry
    @step
    def retry(self):
        """
        This steps runs remotely on AWS batch using 1 virtual CPU and 500Mb of
        memory. Since we are now using a remote metadata service and data
        store, the flow information and artifacts are available from
        anywhere. The step also uses the retry decorator, so that if something
        goes wrong, the step will be automatically retried.
        """
        import boto3
        print(dir(boto3))
        self.message = "Hi from AWS!"
        print("Metaflow says: %s" % self.message)
        from benedict import benedict
        d = benedict(keyattr_dynamic=True) # default False
        d.profile.firstname = "Fabio"
        d.profile.lastname = "Caccamo"
        print(d)
        self.next(self.poetry_demo)

    @poetry()
    @batch(cpu=1, memory=500)
    @step
    def poetry_demo(self):
        """
        This step uses the `poetry` decorator.
        We have included our pyproject.toml and poetry.lock.
        These must be specified as class variables with names:

            `pyproject`: pyproject.toml
            `lockfile`: poetry.lock
        """
        self.message = "Hi from AWS!"
        print("Metaflow says: %s" % self.message)
        from benedict import benedict
        d = benedict(keyattr_dynamic=True) # default False
        d.profile.firstname = "Fabio"
        d.profile.lastname = "Caccamo"
        print(d)
        self.next(self.pip_demo)

    @pip()
    @batch(cpu=1, memory=500)
    @step
    def pip_demo(self):
        """
        This step uses the `pip` decorator.
        We have included our requirements.txt.
        This must be specified as a class variables with the name:

            `requirements`: requirements.txt
        """
        from benedict import benedict
        d = benedict(keyattr_dynamic=True) # default False
        d.profile.firstname = "Fabio"
        d.profile.lastname = "Caccamo"
        print(d)
        self.next(self.extra_deps)
    

    @extra(libraries={"hello": "world", "a": "b"})
    @batch(cpu=1, memory=500)
    @step
    def extra_deps(self):
        """
        This step uses the `extra` decorator.
        This is when we want to include libraries ad-hoc.
        You don't need to use IncludeFile here, just pass in
        the package and it's version in a dict.
        """
        from benedict import benedict
        d = benedict(keyattr_dynamic=True) # default False
        d.profile.firstname = "Fabio"
        d.profile.lastname = "Caccamo"
        print(d)
        self.next(self.end)


    @step
    def end(self):
        """
        The 'end' step is a regular step, so runs locally on the machine from
        which the flow is executed.
        """
        print("HelloAWS is finished.")


if __name__ == "__main__":
  PluginFlow()
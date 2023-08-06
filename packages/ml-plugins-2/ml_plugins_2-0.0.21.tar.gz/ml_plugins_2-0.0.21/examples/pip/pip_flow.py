from metaflow import step, batch, retry
from metaflow.flowspec import FlowSpec
from metaflow.includefile import IncludeFile
from plugins.pip.plugin import pip

class HelloAWSFlow(FlowSpec):
    requirements =  IncludeFile('path', default="./requirements.txt")

    @step
    def start(self):
        """
        The 'start' step is a regular step, so runs locally on the machine from
        which the flow is executed.
        """
        from metaflow import get_metadata

        print("HelloAWS is starting.")
        print("")
        print("Using metadata provider: %s" % get_metadata())
        print("")
        print("The start step is running locally. Next, the ")
        print("'hello' step will run remotely on AWS batch. ")
        print("If you are running in the Netflix sandbox, ")
        print("it may take some time to acquire a compute resource.")

        self.next(self.hello)

    @pip()
    @batch(cpu=1, memory=500)
    @retry
    @step
    def hello(self):
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
        self.next(self.end)

    @step
    def end(self):
        """
        The 'end' step is a regular step, so runs locally on the machine from
        which the flow is executed.
        """
        print("HelloAWS is finished.")


if __name__ == "__main__":
  HelloAWSFlow()
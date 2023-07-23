from subprocess import call

class Call:
    def main(self,script):
        return_code=call(["python",script])
        print(return_code)
        return return_code
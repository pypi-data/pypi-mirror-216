import sys
import json
import datetime


# if __name__ == '__main__':
#     from nwebclient import runner
#     runner.main(custom_job)

class MoreJobs(Exception):
    """ raise MoreJobs([...]) """
    def __init__(self,jobs= []):
        self.data  = {'jobs': jobs}

class JobRunner:
    
    out = lambda msg: "[JobRunner] "+str(msg)
    
    counter = 0 
    
    start = None
    
    def __init__(self, jobexecutor):
        self.jobexecutor = jobexecutor
    def info(self, msg):
        self.out(msg)
    def execute_job(self, job):
        try:
            result = self.jobexecutor(job)
        except MoreJobs as mj:
            result = self.execute_data(mj.data)
        except Exception as e:
            self.info('Error: Job faild', file=sys. stderr)
            result = job
            result['error'] = True
            result['error_message'] = str(s)
        return result
    def execute_data(self.data):
        self.start = datetime.now()
        result = {'jobs': []}
        for job in data['jobs']:
            job_result = self.execute_job(job)
            result['jobs'].append(job_result)
            self.counter = self.counter + 1
        delta = (datetime.now()-self.start).total_seconds() // 60
        self.info("Duration: "+str(delta)+"min")
        return result
    def execute_file(self, infile, outfile = None):
        try:
            data = json.load(open(infile))
            result = self.execute_data(data)
            outcontent = json.dumps(result)
            print(outcontent)
            if not outfile is None:
                with open(outfile, 'w') as f:
                    f.write(outcontent)
        except Exception as e:
            self.info("Error: " + str(e))
            self.info("Faild to execute JSON-File "+str(infile))
    def execute_rest(self, port = 8080):
        self.info("Starting webserver")
        from flask import Flask, render_template, request, response
        from flask import session, copy_current_request_context
        app = Flask(__name__)
        #@app.route('/')
        #def home():
        #    return json.dumps(execute_data(request.form.to_dict(), jobexecutor))
        app.add_url_rule('/', 'home', view_func=lambda: json.dumps(self.execute_data(request.form.to_dict())))
        app.run(host='0.0.0.0', port=port)

class Dispatcher:
    key = 'type'
    runners = {}
    def __init__(self, key='type',**kwargs):
        #for key, value in kwargs.items():
        self.key = key
        self.runners = kwargs
    def __call__(self, data):
        if self.key in data:
            runner = data[self.key]
            return runner(data)
        else:
            return {'success': False, 'message': "Key not in Data", 'data': data}
        
def main(jobexecutor):
    if len(sys.argv)>2:
        infile = sys.argv[1]
        outfile = sys.argv[2]
        runner = JobRunner(jobexecutor)
        if infile == 'rest':
            runner.execute_rest()
        else:
            runner.execute_file(infile, outfile)
    else:
        print("Usage: infile outfile")
        print("Usage: rest api")
        
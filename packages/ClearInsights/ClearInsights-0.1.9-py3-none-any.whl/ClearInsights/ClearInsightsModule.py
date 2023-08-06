import requests
import traceback
import sys
import json

class Logger():
    _apiKey = ""
    _clientSecret = ""
    _applicationName = ""
    def __init__(self, apiKey, clientSecret, applicationName):
        self._apiKey = apiKey
        self._clientSecret = clientSecret
        self._applicationName = applicationName

    def LogError(self, err):
        error = {}
        error['type'] = 'Error'

        if hasattr(err, '__traceback__'):
            stack = traceback.extract_tb(err.__traceback__)
            error['traceback'] = traceback.format_tb(err.__traceback__)
        else:
            stack = traceback.extract_stack()
            error['traceback'] = traceback.format_stack()

        (filename, line, procname, text) = stack[-1]        
        
        error['message'] = str(err)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        self.LogMessage(error)

    def LogCritical(self, err):
        error = {}
        error['type'] = 'Critical'

        if hasattr(err, '__traceback__'):
            stack = traceback.extract_tb(err.__traceback__)
            error['traceback'] = traceback.format_tb(err.__traceback__)
        else:
            stack = traceback.extract_stack()
            error['traceback'] = traceback.format_stack()

        (filename, line, procname, text) = stack[-1]        
        
        error['message'] = str(err)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        self.LogMessage(error)

    def LogInformation(self, err):
        error = {}
        error['type'] = 'Information'

        if hasattr(err, '__traceback__'):
            stack = traceback.extract_tb(err.__traceback__)
            error['traceback'] = traceback.format_tb(err.__traceback__)
        else:
            stack = traceback.extract_stack()
            error['traceback'] = traceback.format_stack()

        (filename, line, procname, text) = stack[-1]        
        
        error['message'] = str(err)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        self.LogMessage(error)

    def LogDebug(self, err):
        error = {}
        error['type'] = 'Debug'

        if hasattr(err, '__traceback__'):
            stack = traceback.extract_tb(err.__traceback__)
            error['traceback'] = traceback.format_tb(err.__traceback__)
        else:
            stack = traceback.extract_stack()
            error['traceback'] = traceback.format_stack()

        (filename, line, procname, text) = stack[-1]        
        
        error['message'] = str(err)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        self.LogMessage(error)

    def LogTrace(self, err):
        error = {}
        error['type'] = 'Trace'

        if hasattr(err, '__traceback__'):
            stack = traceback.extract_tb(err.__traceback__)
            error['traceback'] = traceback.format_tb(err.__traceback__)
        else:
            stack = traceback.extract_stack()
            error['traceback'] = traceback.format_stack()

        (filename, line, procname, text) = stack[-1]        
        
        error['message'] = str(err)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        self.LogMessage(error)

    def LogWarning(self, err):
        error = {}
        error['type'] = 'Warning'

        if hasattr(err, '__traceback__'):
            stack = traceback.extract_tb(err.__traceback__)
            error['traceback'] = traceback.format_tb(err.__traceback__)
        else:
            stack = traceback.extract_stack()
            error['traceback'] = traceback.format_stack()

        (filename, line, procname, text) = stack[-1]        
        
        error['message'] = str(err)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        self.LogMessage(error)

    def LogMessage(self, message):
        URL = "https://clearinsights-ingestion.azurewebsites.net/log/preprocesslog"  
        applicationName = self._applicationName

        framework = "Python " + ".".join([str(sys.version_info.major),str(sys.version_info.minor),str(sys.version_info.micro)])

        HEADERS  = {'apikey':self._apiKey, 'clientsecret':self._clientSecret, 'framework':framework, 'applicationName':applicationName, 'logType':message['type'], 'isPython':"true", }
  
        r = requests.post(url = URL, headers = HEADERS, json= message)

class DynamicMetric:
    _apiKey = ""
    _clientSecret = ""
    _applicationName = ""
    def __init__(self, apiKey, clientSecret, applicationName):
        self._apiKey = apiKey
        self._clientSecret = clientSecret
        self._applicationName = applicationName

    def SendPayload(self, payload):
        URL = "https://clearinsights-ingestion.azurewebsites.net/monitor/savedynamicmetric"  
        applicationName = self._applicationName
        _payload = {}
        _payload["Payload"] = json.dumps(payload)
        HEADERS  = {'apikey':self._apiKey, 'clientsecret':self._clientSecret, 'applicationName':applicationName, 'isPython':"true", }
  
        r = requests.post(url = URL, headers = HEADERS, json= _payload)






   


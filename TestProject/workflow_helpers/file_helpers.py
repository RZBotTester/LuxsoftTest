"""
Helpers to create a different type of test files(extend this by more generators) 
and return a tuple with file name and its base64 content to be used in github api calls

Author: Roman Zanevski
"""
import os, tempfile, base64


class TmpFileCreator:
    '''Create a temporary file class - the ancestor of all file generators'''
    def create_temp_file(self, file_content):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(file_content)
            return temp_file 
    
  
class TextTestFileGenerator(TmpFileCreator):
    '''Create a temporary text file with a given content and return a tuple with file name and its base64 content'''
    def __init__(self):
        self._file_name = 'test.txt'
        self._file_content = 'This is a test file 1, %, $, #, @, !, ^, &, *, (, ), -, +, =, {, }, [, ], |, \, :, ;, ", \', <, >, ?, /, ~, `, ., ,'
        
    def generate_file_name_and_content(self):
        temp_file = self.create_temp_file(self._file_content)
        
        to_base64 = lambda temp_file: base64.b64encode(open(temp_file.name, 'rb').read()).decode('utf-8')
        content = to_base64(temp_file)
        
        temp_file.close()
        os.unlink(temp_file.name)
        
        return self._file_name, content
    

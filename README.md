# NLPMicroService
NLPMicroService repository for NLP Base Model with the Django Simple Example

I designed the base model to handle all NLP Processing Microservice on Django.
To explain the simple structure of the model, I use the **Input, Process, Output** Design to simplifie everything that need to be done on NLP Microservice

### Input
Using the **input_decorator** to handle the file upload or text input,You can either put **.csv** file or **Raw Text** from html and the decorator will handle it for you.

### Process
I don't think i need to do any thing for this part, You can do anything by defining any methods for processing on your NLP Class.

### Output
This is where everything get confusing. First I use the overloading concept(that's actually no supported in vanilla python).
In normal python when you define method in class like this:
```
class SomeClassName:
	def output(self,text):
		print(text + 'hello')
	def output(self,number):
		print(number/2)
```

and when you called
```
SomeClassName.output('hello')
```

I would be raise an error

**TypeError: unsupported operand type(s) for /: 'str' and 'int'**

But, with the **output_method** decorator you can do that and then the class will handle with the parameter inspection for matching the function with the corrrect parameter.
# Usage
### Importing
#### Base Class
- NLPBase
#### 2 Decorators
- input_method
- output_method
```
from NLPApp.NLPBase import NLPBase,input_method,output_method
```

### Use Case
#### Base Class
You can inherit the base class to any class you want
#### Decorators
Use the decorators to mark the **Input** and **Output** Method
```
class YourClassName(NLPBase):
	@input_method
	def getText(self,text):
		pass
		
	def process(self,some_params):
		pass
		
	@output_method
	def output(self,df:'DataFrame'):
		pass
```

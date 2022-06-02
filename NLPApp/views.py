import urllib,base64,io,pydotplus
from django.shortcuts import render
from django.http import HttpResponse
from NLPApp.NLPBase import NLPBase,input_method,output_method
import pandas as pd
import matplotlib.pyplot as plt
import rdflib
from rdflib import URIRef,RDF,Literal
from rdflib.namespace import FOAF
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage

# Create your views here.

def home(request):
	return render(request,'NLPApp/home.html')

class RDF(NLPBase):
	@input_method
	def process(self,df):
		g = rdflib.Graph()

		for idx,row in df.iterrows():
			g.add(tuple([eval(item) for item in row.values]))

		return g
		
	
	@output_method
	def output(self,g:'Graph'):
		'''
		This is Graph-type overloading methods
		'''
		G = rdflib_to_networkx_multidigraph(g)

		# Plot Networkx instance of RDF Graph
		pos = nx.spring_layout(G, scale=2)
		edge_labels = nx.get_edge_attributes(G, 'r')
		nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
		nx.draw(G, with_labels=True)

		fig=plt.gcf()
		buf = io.BytesIO()
		fig.savefig(buf,format='png')
		buf.seek(0)
		string = base64.b64encode(buf.read())
		uri= urllib.parse.quote(string)
		return uri

	@output_method
	def output(self,string:str):
		'''
		This is string-type overloading method
		'''
		return string[::-1]

def rdf(request):
	return render(request,'NLPApp/RDF.html')

def getText(request):
	rdf = RDF()
	graph_img = rdf.output(rdf.process(request.FILES['myfile']))
	string = rdf.output('Hello World')


	return render(request,'NLPApp/result.html',{'graph_img':graph_img,'r_txt':string})
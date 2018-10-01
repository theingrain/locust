import re
import os
import csv
import plotly
import random
import shutil
import datetime
import fileinput
import pandas as pd
from yattag import Doc
import plotly.graph_objs as go
import plotly.figure_factory as FF

class RequestDescriptor :

	def generate_logs_from_existing_jenkins_logs(self, jenkins_logs) :
		jenkins_logs = open(jenkins_logs)
		if not os.path.exists('reports'):
			os.makedirs('reports')
		generated_logs = open(os.path.join('reports','request_time_logs.txt'), 'w')
		pattern = r'Name[^\r\n]+((\r|\n|\r\n)[^\r\n]+)*Total(.*)'
		regex = re.compile(pattern, re.IGNORECASE)
		for match in regex.finditer(jenkins_logs.read()):
			match.start()
			generated_logs.write(match.group(0) + '\n')
		generated_logs.close()
		jenkins_logs.close()

	def create_dict_for_api_time_graph(self) :
		api_list = []
		time_graph_dict = {}
		with open(os.path.join('reports','request_time_logs.txt'), 'rU') as file_data :
			for line in file_data:
				line = line.split()
				if line[0] == 'POST' and len(line) <= 10 :
					api_list.append(line[1])
					api_list = list(set(api_list))
		for api in api_list :
			request_rates = []
			time_graph_dict[api] = request_rates
			with open(os.path.join('reports','request_time_logs.txt'), 'rU') as file_data:
				for line in file_data :
					line = line.split()
					if line[0] == 'POST' and len(line) == 10 and line[1] == api :
						request_rates.append(line[9])
		return time_graph_dict


class CSVUtil :

	def create_csv_for_graph(self, time_graph_dict) :
		with open(os.path.join('reports','request_time_data.csv'), 'w') as csvfile:
			filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			headings = ['Seconds']
			apis_list = list(time_graph_dict.keys())
			headings = headings + apis_list
			filewriter.writerow(headings)
			for items in range(0, len(time_graph_dict.get(apis_list[0]))) :
				data = [items]
				for values in apis_list :
					data.append(time_graph_dict.get(values)[items])
				filewriter.writerow(data)

	def edit_with_spaces(self, spaces, location, filename) :
		original_location = filename + '.csv'
		report_location = os.path.join('reports/', filename + '.csv')
		read_file = open(original_location, 'r')
		write_file = open(report_location, 'w')
		csv_reader = csv.reader(read_file)
		csv_writer = csv.writer(write_file)
		for line in csv_reader :
			for space in range(0, spaces) :
				line.insert(location, ' ')
			csv_writer.writerow(line)

class FiguresGenerator :
	def time_graph_for_requests_throughput(self, time_graph_dict) :
		data_file = pd.read_csv(os.path.join('reports','request_time_data.csv'))
		data = []
		plotting_color_count = len(list(time_graph_dict.keys()))
		color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(plotting_color_count)]
		for value in list(time_graph_dict.keys()) :
			trace = go.Scatter(
						x=data_file.Seconds,
                		y=data_file[value],
                		name = value,
                		line = dict(color = str(color[plotting_color_count - 1])),
                		opacity = 0.8)
			plotting_color_count = plotting_color_count - 1
			data.append(trace)
		layout = dict(
			title = "Throughput Graph for " + datetime.date.today().strftime('%d, %b %Y'),
			xaxis = dict( title='Time in Seconds', range = [0,len(time_graph_dict.get(list(time_graph_dict.keys())[0]))]),
			yaxis = dict(title='Requests Count')
			)
		fig = dict(data=data, layout=layout)
		# plotly.offline.plot(fig, filename='reports//request_time.html', auto_open=False)
		return plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

	def time_graph_for_requests_completion(self) :
		xaxis_data = []
		trace = []
		with open('responses_distribution.csv') as csv_file :
			csv_reader = csv.reader(csv_file, delimiter=',')
			for line in csv_reader :
				for index in range(2, len(line)) :
					xaxis_data.append(line[index])
				break
			for line in csv_reader :
				yaxis_data = []
				api_name = None
				if line[0] == 'Name' or line[0] == 'Total' :
					continue
				else :
					for index in range(2, len(line)) :
						yaxis_data.append(line[index])
					api_name = line[0].split()[1]
					trace_data = go.Bar(
						x = xaxis_data,
						y = yaxis_data,
						name = api_name
						)
					trace.append(trace_data)
		layout = go.Layout(
			barmode = 'group',
			title = "Requests Distribution Graph for " + datetime.date.today().strftime('%d, %b %Y'),
			xaxis = dict( title='Requests Completed(%)'),
			yaxis = dict( title='Time(ms)')
			)
		fig = go.Figure(data=trace, layout=layout)
		return plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

	def create_table_from_csv(self, filename) :
		df = pd.read_csv(os.path.join('reports',filename + '.csv'))
		df_external_source = FF.create_table(df.head(), height_constant = 40)
		return plotly.offline.plot(df_external_source, include_plotlyjs=False, output_type='div')

class ReportGenerator :

	def create_dashboard(self, div_for_throughput, div_for_throughput_graph, div_for_distribution, div_for_distribution_graph) :
		shutil.copy(os.path.join('reports','templates','dashboard_template.html'),
			os.path.join('reports','dashboard_summary.html'))
		update_data = div_for_throughput + '\n' + div_for_throughput_graph + '\n' + div_for_distribution + '\n' + div_for_distribution_graph
		with open(os.path.join('reports','dashboard_summary.html'), 'r') as file :
			filedata = file.read()
		filedata = filedata.replace('{{div_data}}', update_data)
		with open(os.path.join('reports','dashboard_summary.html'), 'w') as file:
			file.write(filedata)
		self.manipulate_html_dashboard()

	def manipulate_html_dashboard(self) :
		with open(os.path.join('reports','dashboard_summary.html'), 'r') as file:
			filedata = file.read()
		pattern = r'<b> .[0-9]<\/b>'
		regex = re.compile(pattern, re.IGNORECASE)
		for match in regex.finditer(filedata):
			match.start()
			filedata = filedata.replace(match.group(0), '<b> </b>')
		filedata = filedata.replace('Median response time', 'Median <br>response <br>time')
		filedata = filedata.replace('Average response time', 'Average <br>response <br>time')
		filedata = filedata.replace('Min response time', 'Min <br>response <br>time')
		filedata = filedata.replace('Max response time', 'Max <br>response <br>time')
		filedata = filedata.replace('Average Content Size', 'Average <br>Content <br>Size')
		filedata = filedata.replace('"showLink": true', '"showLink": false')
		with open(os.path.join('reports','dashboard_summary.html'), 'w') as file:
			file.write(filedata)

	def get_email_template_src(self):
		doc, tag, text = Doc().tagtext()
		doc.asis('<!DOCTYPE html>')
		with tag('html'):
			with tag('head'):
				with tag('title'):
					text('Summary Report')
				doc.asis('<meta charset="utf-8" />')
			with tag('body'):
				with tag('h4'):
					text('APIs STATISTICS')
				with tag('blockquote'):
					with tag('table', style='font-size: 12px;width: 100%;border-spacing: 2px;border-color:grey'):
						with tag('thead', style="width: 100%;border-spacing: 2px;border-color:grey"):
							with tag('tr'):
								with tag('th', colspan='11', style='font-size: 14px;border: 1px #6ea1cc !important;text-align: center; padding: 8px;background-color: #508abb;color: #fff;'):
									text('STATISTICS FOR ' + datetime.date.today().strftime('%d, %b %Y'))
							with tag('tr'):
								with open('responses_requests.csv') as csv_file:
									csv_reader = csv.reader(csv_file, delimiter=',')
									line_count = 0
									for row in csv_reader:
										for elements in range(0, len(row)):
											if elements in [4, 8]:
												continue
											with tag('th', style='font-size: 14px;border: 1px #6ea1cc !important;text-align: left; padding: 8px;background-color: #508abb;color: #fff;'):
												text(row[elements])
										break
								with open('responses_distribution.csv') as csv_file:
									csv_reader = csv.reader(csv_file, delimiter=',')
									line_count = 0
									for row in csv_reader:
										for elements in range(0, len(row)):
											if elements in [6, 7, 9]:
												with tag('th', style='font-size: 14px;border: 1px #6ea1cc !important;text-align: left; padding: 8px;background-color: #508abb;color: #fff;'):
													text(row[elements])
										break
						with tag('tbody', style='font-size: 12px;'):
							with open('responses_requests.csv') as csv_file, open('responses_distribution.csv') as temp_csv_file:
								csv_reader = csv.reader(csv_file, delimiter=',')
								temp_csv_reader = list(csv.reader(temp_csv_file, delimiter=','))
								line_count = 0
								temp_line_count = 0
								counter = 0
								for row in csv_reader:
									temp_row = temp_csv_reader[counter]
									counter = counter + 1
									if line_count == 0 or row[0] == 'None' or temp_line_count == 0 or temp_row[0] == 'Total':
										line_count = line_count + 1
										temp_line_count = temp_line_count + 1
										continue
									else :
										with tag('tr', style='width: 100%;border-bottom:1px solid #efefef;border-top:1px solid #ececec;background-color:#f4fbff;'):
											for elements in range(0, len(row)):
												if elements in [4, 8]:
													continue
												with tag('td', style='border-collapse:collapse;text-align: left; padding: 8px'):
													text(row[elements])
											for temp_elements in range(0, len(temp_row)):
												if temp_elements in [6,7,9]:
													with tag('td', style='border-collapse:collapse;text-align: left; padding: 8px'):
														text(temp_row[temp_elements])

						with tag('tfoot'):
							with open('responses_requests.csv') as csv_file, open('responses_distribution.csv') as temp_csv_file:
								csv_reader = csv.reader(csv_file, delimiter=',')
								temp_csv_reader = list(csv.reader(temp_csv_file, delimiter=','))
								counter = 0
								for row in csv_reader:
									temp_row = temp_csv_reader[counter]
									counter = counter + 1
									if row[0] == 'None':
										with tag('tr', style='width: 100%;border-spacing: 2px;background-color:#fcffc9 !important'):
											for elements in range(0, len(row)):
												if elements in [4, 8]:
													continue
												with tag('td', style='border-collapse:collapse;text-align: left; padding: 8px'):
													text(row[elements])
											for temp_elements in range(0, len(temp_row)):
												if temp_elements in [6,7,9]:
													with tag('td', style='border-collapse:collapse;text-align: left; padding: 8px'):
														text(temp_row[temp_elements])
									else :
										continue
		return doc.getvalue()

	def write_email_src_to_file(self, src_script):
		with open(os.path.join('reports','email_summary.html'), 'w') as file:
			file.write(src_script)
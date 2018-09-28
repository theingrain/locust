import sys
import packages.reporter as util

def generate_dashboard(jenkins_logs) :
	util.CSVUtil().edit_with_spaces(3, 2, 'responses_requests')
	util.CSVUtil().edit_with_spaces(3, 1, 'responses_distribution')
	div_for_throughput = util.FiguresGenerator().create_table_from_csv('responses_requests')
	div_for_distribution = util.FiguresGenerator().create_table_from_csv('responses_distribution')
	util.RequestDescriptor().generate_logs_from_existing_jenkins_logs(jenkins_logs)
	graph_plots = util.RequestDescriptor().create_dict_for_api_time_graph()
	util.CSVUtil().create_csv_for_graph(graph_plots)
	div_for_throughput_graph = util.FiguresGenerator().time_graph_for_requests_throughput(graph_plots)
	div_for_distribution_graph = util.FiguresGenerator().time_graph_for_requests_completion()
	util.ReportGenerator().create_dashboard(div_for_throughput, div_for_throughput_graph, div_for_distribution, div_for_distribution_graph)

generate_dashboard(str(sys.argv[1]))
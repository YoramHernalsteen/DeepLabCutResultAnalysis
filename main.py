import utils.csv_utils as csv_utils
import analysis.density_analysis as density_analysis
import analysis.path_analysis as path_analysis

from terminal.terminal import Terminal

def main():
    #csv_file = '/Users/yoramhernalsteen/Projects/Python/dlc_pixel_analyser/data/test_data.csv'
    #data = csv_utils.read_body_part('centre', csv_file)
    #density_analysis.plot_density_map_continous(data)
    #path_analysis.trace_path(data)

    terminal = Terminal()
    terminal.run()

    


if __name__ == "__main__":
    main()

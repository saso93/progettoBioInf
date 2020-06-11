import os
# to suppress the annoying logging of tensorlow
# 0 = all messages are logged (default behavior)
# 1 = INFO messages are not printed
# 2 = INFO and WARNING messages are not printed
# 3 = INFO, WARNING, and ERROR messages are not printed
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

from data_processing import *
from results import *
from setup_models import *
from training_models import *

logging.getLogger(__name__)

logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def main():
    logging.info('Started')

    cell_lines = ["K562"]
    assembly = "hg19"
    window_size = 200

    for cell_line in cell_lines:
        logging.info('Cell Line: ' + cell_line)

        # Step 0. Initial Setup
        logging.info('Step 0. Initial Setup')
        initial_setup(cell_line)

        # Step 1. Data Retrieval
        logging.info('Step 1. Data Retrieval')
        if are_data_retrieved(cell_line):
            logging.info('Data already retrieved! Load from .csv files...')
            epigenomes, labels, sequences = load_csv_retrieved_data(cell_line)
        else:
            epigenomes, labels, sequences = dataRetrieval(cell_line, assembly, window_size)

        # Step 2. Data Elaboration
        logging.info('Step 2. Data Elaboration')
        if are_data_elaborated(cell_line):
            logging.info('Data already elaborated! Load from .csv files...')
            epigenomes = load_csv_elaborated_data(cell_line)
        else:
            epigenomes = dataElaboration(epigenomes, labels, cell_line)

        # Step 3. Data Visualization
        logging.info('Step 3. Data Visualization')
        if are_data_visualized(cell_line):
            logging.info("Data already visualized! Skip the step...")
        else:
            data_visualization(epigenomes, labels, sequences, cell_line)

        # Step 4. Training the models
        logging.info("Step 4. Training the models")

        for region, x in epigenomes.items():
            if os.path.exists('json/' + cell_line + '/results_' + region + ".json"):
                logging.info("Results " + region + " ok!")

            else:
                logging.info("Step 4.1 Training Tabular Data" + region)
            
                labels = labels[region].to_numpy().ravel()
                logging.info("labels shape: " + ''.join(str(labels.shape)))
                epigenomes = cleanup_epigenomics_data(epigenomes, region)
                logging.info("Setup models for Tabular Data: " + region)
                # list of models, args for training, indeces train/test, num splits
                #models, kwargs, holdouts, splits = setup_models_ffnn(epigenomes.shape[1])
                #training_the_models(holdouts, splits, models, kwargs, epigenomes, labels, cell_line, region)
               
                logging.info("Step 4.2 Training Sequence Data" + region)
                
                #TODO da modificare completamente! i dati di sequenza erano sbagliati!!!!
                sequences = cleanup_sequences_data(sequences, region)
                logging.info("Setup models for Sequence Data: " + region)

                models, kwargs, holdouts, splits = setup_model_cnn(sequences.shape)
                training_the_models(holdouts, splits, models, kwargs, sequences, labels, cell_line, region)

        
        # Step 5. Results and statistical tests
        #TODO
        logging.info("TODO!!! Step 5. Results and statistical tests")
        # results = get_results(holdouts, splits, models, kwargs, X, y)
        # results_df = convert_results_to_dataframe(results)
        # save_results_df_to_csv(results_df)
        # save_barplots_to_png()

        # TODO aggiungi test statistici e plot dei risultati

        logging.info('Exiting cell_line' + cell_line)


if __name__ == '__main__':
    main()

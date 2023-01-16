import json
import csv


class FlawFilesValidator:
    def __init__(self, file_name):
        self.fileName = file_name
        results = open(self.fileName)
        resultRows = results.readlines()
        # remove line breaks (\n) from each resultRow and convert the object returned by map() to a list
        resultRows = list(map(lambda resultRow: resultRow.rstrip(), resultRows))
        self.headerRow = resultRows[0]
        self.dataRows = resultRows[1:]        
        self.validate_data_file()

    def generate_summary_data(self):
        dictionary_data_rows = list(map(lambda dataRow: self.convert_data_row_to_dictionary(dataRow), self.dataRows))
        return json.dumps(dictionary_data_rows)

    def generate_data_row_in_json_format(self, row_number):  
        self.validate_row_number(row_number)    
        return json.dumps(self.convert_data_row_to_dictionary(self.dataRows[row_number-1]))
    
    def generate_data_row_in_csv_format(self, row_number):
        self.validate_row_number(row_number)        
        return json.dumps(self.dataRows[row_number-1])
    
    def generate_python_in_memory_representation(self, rowNumber): 
        self.validate_row_number(rowNumber)
        return self.dataRows[rowNumber-1].split(",")

    def create_summary_json_file(self):
      dictionaryDataRows = list(map(lambda dataRow: self.convert_data_row_to_dictionary(dataRow), self.dataRows))      
      jsonFileName = self.fileName.split('.flaw')[0] + '.json' 
      with open(jsonFileName, 'w') as outfile:
          json.dump(dictionaryDataRows, outfile)

    def create_row_data_files(self, rowNumber):
        self.validate_row_number(rowNumber)  
        self.create_json_file(rowNumber)
        self.create_csv_file(rowNumber)      
        
    def create_json_file(self, rowNumber):
        self.validate_row_number(rowNumber)  
        jsonFileName = self.fileName.split('.flaw')[0] + '_row' + str(rowNumber) + '.json'
        with open(jsonFileName, 'w') as outfile:
            dictionaryDataRow = self.convert_data_row_to_dictionary(self.dataRows[rowNumber-1])
            json.dump(dictionaryDataRow, outfile)

    def create_csv_file(self, rowNumber):
        self.validate_row_number(rowNumber) 
        csvFileName = self.fileName.split('.flaw')[0] + '_row' + str(rowNumber) + '.csv'
        with open(csvFileName, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.headerRow.split(","))
            writer.writerow(self.dataRows[rowNumber-1].split(","))

    def convert_data_row_to_dictionary(self, dataRow):
        splittedDataRow = dataRow.split(",")
        dictionary = {}
        dictionary['experiment_name'] = splittedDataRow[0]
        dictionary['sample_id'] = int(splittedDataRow[1])
        dictionary['flawness'] = float(splittedDataRow[2])
        dictionary['category_guess'] = splittedDataRow[3]
        return dictionary
        
    def validate_row_number(self, rowNumber):
        if (not (type(rowNumber) is int and rowNumber <= len(self.dataRows))):
            raise Exception("The provided row number is invalid or does not exist. Please provide another row number.")
      
    def validate_data_file(self):
        self.validate_header()

        # rejects files with valid header but without data
        if (len(self.dataRows) == 0):
          raise Exception("The file does not contain data.")

        for dataRow in self.dataRows:
            self.validate_data_row(dataRow)

    # check if header subtitles are correctly spelled and displayed in the expected order
    def validate_header(self):
        validSplittedHeader = "experiment_name,sample_id,flawness,category_guess"
        if self.headerRow.replace(" ", "") != validSplittedHeader:
          raise Exception("The file header is invalid.")
       
    # check if each row data is provided, valid and displayed in the expected order
    def validate_data_row(self, dataRow):
        splittedDataRow = dataRow.split(",")
        if (len(splittedDataRow) != 4):
            raise Exception("Row data has an invalid number of fields.")

        self.validate_experiment_name(splittedDataRow[0])
        self.validate_sample_id(splittedDataRow[1])
        self.validate_flawness(splittedDataRow[2])
        self. validate_category_guess(splittedDataRow[3])

    # check if experimentName is of type string and is not empty
    def validate_experiment_name(self, experimentName):
        if not (type(experimentName) is str and experimentName != ""):
          raise Exception("The experiment name data is invalid.")

    # check if sampleId is of type integer and positive integer
    def validate_sample_id(self, sampleId):
        # convert string to int and deal with error if the string cannot be converted to int
        try:
            sampleId = int(sampleId)
            if sampleId < 0:
              raise Exception("The sample id value is not a positive integer {sampleId}.")
        except ValueError:
              raise Exception("The sample id value is not an integer.")

    # check if flawness is of type float within 0.0 and 1.0
    def validate_flawness(self, flawness):
        # convert string to float and deal with error if the string string cannot be converted to float
        try:
            flawness = float(flawness)
            if not (0.0 <= flawness <= 1.0):
              raise Exception("The flawness value is not a value between 0.0 and 1.0.")
        except ValueError:
              raise Exception("The flawness value is not a float.")

    # check if categoryGuess has one of the expected values for this field
    def validate_category_guess(self, categoryGuess):
        validCategoriesGuess = {"real", "fake", "ambiguous"}
        # assuming categoryGuess must be case-sensitive and match one of the items in validCategoriesGuess
        if not categoryGuess in validCategoriesGuess:
          raise Exception("The category guess is not valid.")


# Instantiate an object of FlawFilesValidator class
flaw = FlawFilesValidator('file_1.flaw')

# Printing data for testing purposes 
print(flaw.generate_summary_data())
print(flaw.generate_data_row_in_json_format(2))
print(flaw.generate_data_row_in_csv_format(2))
print(flaw.generate_python_in_memory_representation(2))

# invoking extra methods to create .json and .csv files
flaw.create_row_data_files(2)
flaw.create_summary_json_file()



#print(flaw.validate_flawness("2.1"))
#print(flaw.validate_sample_id("-1"))
#print(flaw.validate_experiment_name("fwtey"))
#print(flaw.validate_category_guess("real"))

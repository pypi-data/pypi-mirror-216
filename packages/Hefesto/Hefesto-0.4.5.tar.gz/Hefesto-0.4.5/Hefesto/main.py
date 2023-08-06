import pandas as pd
from perseo.main import milisec
# from template import Template
from Hefesto.template import Template
import sys
import yaml
import math
import requests
import logging

class Hefesto():

    def __init__(self, datainput, reset = False):
        # Import data input:
        if not reset:
            try:
                self.df_data = pd.read_csv(datainput)
            except FileNotFoundError:
                raise FileNotFoundError(f"File '{datainput}' does not exist.")
            finally:
                self.df_data = self.df_data.where(pd.notnull(self.df_data), None)
        else:
            self.df_data = datainput
            return self.df_data
        
        # Create an object as dictonary to reduce duplicate calls:
        self.reg = dict()

    def transformFiab(self):

    # Import static template for all CDE terms:
        temp = Template.template_model

    # Check the status of the dataframe used:
        if not "model" and "pid" and "value" in self.df_data.columns:
            sys.exit(" The quality of the data used in not correct, please check CSV used to perform the transformation.")

    # Empty objects:
        resulting_df = pd.DataFrame()
        row_df = {}


        for row in self.df_data.iterrows():
            milisec_point = milisec()

            # Tag each row with the new of the model 
            new_row = {milisec_point : {"model": row[1]["model"]}}
            row_df.update(new_row)

            # Include columns related to ontological terms:
            for cde in temp.items():
                if cde[0] == row_df[milisec_point]["model"]:
                    row_df[milisec_point].update(cde[1])
                    # print(row_df[milisec_point])

            # Include columns from input CSV table:
            for title, val in row[1].items():
                if not val == None:
                    row_df[milisec_point].update({title:val})

            # Concate rows:
            final_row_df = pd.DataFrame(row_df[milisec_point], index=[1])
            resulting_df = pd.concat([resulting_df, final_row_df])

        # Reset Index:    
        resulting_df = resulting_df.reset_index(drop=True)
        # Turn any nan to None:
        resulting_df = resulting_df.where(pd.notnull(resulting_df), None)

        # Value edition:
        resulting_df = self.valueEdition(resulting_df)
        # Clean blanks:
        resulting_df = self.cleanBlanks(resulting_df)

        # uniqid generation:
        resulting_df['uniqid'] = ""
        for i in resulting_df.index:
            resulting_df.at[i, "uniqid"] = milisec()

        print("Structural transformation: Done")
        new = Hefesto.__init__(self, datainput= resulting_df, reset = True)
        return new

    def transformShape(self,configuration, uniqid_generation= True, contextid_generation= True, clean_blanks= False):

        if type(configuration) is not dict:
            sys.exit("configuration file must be a dictionary from a Python, YAML or JSON file")

        
        # Import static template for all CDE terms:
        temp = Template.template_model
        
        # Empty objects:
        resulting_df = pd.DataFrame()
        row_df = {}

        # Iterate each row from data input
        # check each YAML object from configuration file to set the parameters
        for row in self.df_data.iterrows():

            for config in configuration.items():

                # Create a unique stamp per new row to about them to colapse:
                milisec_point = milisec()

                row_df.update({milisec_point: {'model':config[1]["cde"]}})
                
                # Add YAML template static information
                for cde in temp.items():
                    if cde[0] == row_df[milisec_point]["model"]:
                        row_df[milisec_point].update(cde[1])

                # Relate each YAML parameter with original data input
                for element in config[1]["columns"].items():
                    for r in row[1].index:
                        if r == element[1]:
                            dict_element = {element[0]:row[1][r]}
                            row_df[milisec_point].update(dict_element)
                            

                # Store formed element into the final table:
                final_row_df = pd.DataFrame(row_df[milisec_point], index=[1])
                resulting_df = pd.concat([resulting_df, final_row_df])

        # Reset Index:    
        resulting_df = resulting_df.reset_index(drop=True)
        # Turn any nan to None:

        resulting_df = resulting_df.where(pd.notnull(resulting_df), None)


        # Value edition:
        resulting_df = self.valueEdition(resulting_df)
        resulting_df = resulting_df.where(pd.notnull(resulting_df), None)


        # Clean blanks:
        resulting_df = self.cleanBlanks(resulting_df)
        # uniqid generation:
        # print(resulting_df)

        resulting_df['uniqid'] = ""
        for i in resulting_df.index:
            resulting_df.at[i, "uniqid"] = milisec()

        
        print("Structural transformation: Done")
        new = Hefesto.__init__(self, datainput= resulting_df, reset = True)
        return new

    def cleanBlanks(self, resulting_df): # TODO solve the attribute_type value problem

        for row_final in resulting_df.iterrows():
            if row_final[1]["value"] == None and row_final[1]["valueIRI"] == None and row_final[1]["comments"] == None and row_final[1]["agent_id"] == None and row_final[1]["target_type"] == None:
                resulting_df = resulting_df.drop(row_final[0])
        del resulting_df["value"]
        del resulting_df["valueIRI"]

        return resulting_df

    def valueEdition(self, resulting_df):

        # valueIRI 
        valueRelation = {
            "Sex":"attribute_type",
            "Status":"attribute_type",
            "Diagnosis":"attribute_type",
            "Genetic":"value_id",
            "Symptoms":"attribute_type",
            "Imaging":"value_id",
            "Clinical_trial":"attribute_type"
        }
        # Datatype:
        datatypeRelation = {
            "xsd:string":"value_string",
            "xsd:date" : "value_date",
            "xsd:float": "value_float",
            "xsd:integer":"value_integer"
        }
        modelList = ["Deathdate","First_Visit","Symptoms_onset"]
        
        # Value edition:
        for index, row in resulting_df.iterrows():
            for k,v in datatypeRelation.items():
                
                # value ---> value_DATATYPE:
                if row["value_datatype"] == k:
                    resulting_df.at[index, v] = resulting_df["value"][index]
                    resulting_df = resulting_df.where(pd.notnull(resulting_df), None)

            for k,v in valueRelation.items():
                # valueIRI ---> attribute_id/value:
                if row["model"] == k:
                    resulting_df.at[index, v] = resulting_df["valueIRI"][index]
                    resulting_df = resulting_df.where(pd.notnull(resulting_df), None)

            # attribute_id_value
            # if row["model"] == "Genetic":
            #     resulting_df.at[index, "attribute_id_value"] = resulting_df["value"][index]
            #     resulting_df.at[index, "value_string"] = None # Deleting the value_string in case it moves from value to value_string
            #     resulting_df = resulting_df.where(pd.notnull(resulting_df), None)

            # Pass value date into date context
            if row["value"] != None and row["value_datatype"] == "xsd:date":
                resulting_df.at[index, "date"] = resulting_df["value"][index]
                resulting_df = resulting_df.where(pd.notnull(resulting_df), None)

            # Pass value age into age context
            if row["value"] != None and row["value_datatype"] == "xsd:float" and row["model"] in modelList:
                resulting_df.at[index, "age"] = resulting_df["value"][index]
                resulting_df = resulting_df.where(pd.notnull(resulting_df), None)

            # Move startdate of diagnosis to date context
            if row["model"] == "Diagnosis":
                resulting_df.at[index, "date"] = resulting_df["startdate"][index]
                resulting_df = resulting_df.where(pd.notnull(resulting_df), None)

            # enddate correction:
            if row["startdate"] != None and row["enddate"] == None:
                resulting_df.at[index,"enddate"] = resulting_df["startdate"][index]
                resulting_df = resulting_df.where(pd.notnull(resulting_df), None)

        return resulting_df

    def get_uri(self, col, ont):

        
        if not col in list(self.df_data.columns):
            sys.exit("ERROR: selected column doesnt exist")

        # Column duplication to work in new column:
        self.df_data[col+"_uri"] = self.df_data.loc[:, col]
        

        # Loop throught new column to replace current value with API term:
        for i in self.df_data[col+"_uri"].index:
            term = self.df_data.at[i,col+"_uri"]
            if term in self.reg:
                self.df_data.at[i,col+"_uri"] = self.reg[term] 

            else: # API call to OLS
                url= "http://www.ebi.ac.uk/ols/api/search?q="+ term +"&ontology=" + ont
                r = requests.get(url,headers= {"accept":"application/json"})
                data = r.json()
                # JSON navigation:
                try:
                    data_iri = data["response"]["docs"][0]["iri"]
                except IndexError:
                    data_iri = "NOT MATCH"
                # Attach new value to the Dataframe:
                self.reg[term] = data_iri
                self.df_data.at[i,col+"_uri"] = data_iri 

        print("URLs from Label calling: Done")
        new = Hefesto.__init__(self, datainput= self.df_data, reset = True)
        return new

    def get_label(self, col):

        # Column duplication to work in new column:
        self.df_data[col+"_label"] = self.df_data.loc[:, col]

        # Loop throught new column to replace current value with API term:
        for i in self.df_data[col+"_label"].index:
            term = self.df_data.at[i,col+"_label"]
            if term in self.reg:
                self.df_data.at[i,col+"_label"] = self.reg[term] 

            else: # API call to OLS
                url= 'http://www.ebi.ac.uk/ols/api/terms?iri='+ term
                r = requests.get(url,headers= {"accept":"application/json"}) # API call to OLS
                data = r.json()
                # JSON navigation:
                try:
                    data_label = data["_embedded"]["terms"][0]["label"]
                except TypeError:
                    data_label = "NOT MATCH"
                # Attach new value to the Dataframe:
                self.reg[term] = data_label
                self.df_data.at[i,col+"_label"] = data_label 

        print("Labels from URL calling: Done")
        new = Hefesto.__init__(self, datainput= self.df_data, reset = True)
        return new

    def replacement(self, col, key, value, duplicate = False):

        if duplicate == "True":
            # Column duplication to work in new column:
            self.df_data[col+"_dup"] = self.df_data.loc[:, col]
            self.df_data[col+"_dup"] = self.df_data[col+"_dup"].replace([key],value)
        else:
            self.df_data[col] = self.df_data[col].replace([key],value) 

        print("Replacement from " + key + "to "+ value + " at column " + col +": Done")
        new = Hefesto.__init__(self, datainput= self.df_data, reset = True)
        return new
        

# # Test 1:

# test = Hefesto(datainput = "../data/INPUT_DATA.csv")
# transform = test.transformFiab()
# transform.to_csv ("../data/OUTPUT_DATA.csv", index = False, header=True)

# Test 2
# with open("../data/CDEconfig.yaml") as file:
#     configuration = yaml.load(file, Loader=yaml.FullLoader)

# test = Hefesto(datainput = "../data/INPUT_DATA2.csv")
# transform = test.transformShape(configuration=configuration, clean_blanks = True) #, clean_blanks=False
# # label = test.get_label("output_type")
# # url_from_label= test.get_uri("output_type_label","ncit")
# # repl= test.replacement("output_type_label", "Date","DateXXX", duplicate=False)
# transform.to_csv ("../data/OUTPUT_DATA2.csv", index = False, header=True)
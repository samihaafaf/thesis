#!/usr/bin/env python3

from SequenceEncoder import SequenceEncoder
from tqdm.contrib.concurrent import thread_map
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import time
from Bio import SeqIO
from pathlib import Path
from functools import partial


class DatasetBuilder:
    def __init__(self, root=None, family_path=None, max_workers=10, limit=False, limit_size=500):
        if root and family_path:
            self.root = root
            self.family_path = family_path
            self.paths_list = ['train', 'test']
            self.families = list(self.family_path.keys())
            self.max_workers = max_workers
            self.limit=limit
            self.limit_size=limit_size
            self.createDirStructure()
        else:
            print("Error")

    def run(self):
        for family, path in self.family_path.items():
            print("\n\n\n==================================================================")
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>> {family} <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            df = self.fastaToDataFrame(path)
            self.createImages(df, family)
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>> {family} Done <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print("==================================================================\n\n\n")


    def createDirStructure(self):
        print("######################## Folder Creation ########################\n")
        root = Path(self.root)
        for path in self.paths_list:
            for family in self.families:
                full_path = root / path / family
                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                    print(f"{full_path} has been created")
                else:
                    print(f"{full_path} already exists, Skipping")
        print("\n######################## Folder Creation Done ####################")


    def fastaToDataFrame(self, path):
        print("######################## Fasta To DataFrame ######################\n")
        name = []
        sequence = []
        for record in SeqIO.parse(path, 'fasta'):
            name.append(record.name)
            sequence.append(str(record.seq))

        if self.limit:
            name = name[:self.limit_size]
            sequence = sequence[:self.limit_size]

        name_series = pd.Series(name)
        sequence_series = pd.Series(sequence)

        df = pd.DataFrame({'name': name_series, 'sequence': sequence_series})
        print(f"Successfully parsed {path}")
        print("\n#################### Fasta To DataFrame Finished #################")

        return df


    def encoder(self, row, path, family):
        SequenceEncoder(seq=row[2]).save(f"{self.root}/{path}/{family}/{row[1]}")


    def createImages(self, df, family):
        print("########################### Train Test Split #####################\n")
        train, test = train_test_split(df, test_size=0.3)
        print("Successfully splited the Dataframe")
        print("\n###################### Train Test Split Done #####################")

        print(f"##################### Converting train/{family} #######################\n")
        thread_map(partial(self.encoder, path='train', family=family), train.itertuples(), max_workers=self.max_workers, total=train.shape[0])
        print(f"\n##################### Converting train/{family} Done ##################")

        print(f"##################### Converting test/{family} ########################\n")
        thread_map(partial(self.encoder, path='test', family=family), test.itertuples(), max_workers=self.max_workers, total=test.shape[0])
        print(f"\n##################### Converting test/{family} Done ###################\n")





if __name__=="__main__":
    root = './datasets'
    family_path = {
            'PVP': './binary_seq/pvp.fa',
            'non-PVP': './binary_seq/non_pvp.fa'
            }

    DatasetBuilder(root, family_path, max_workers=5, limit=True, limit_size=2000).run()



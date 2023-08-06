import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pylcs

absolute_path = os.fspath(Path.cwd().parent.parent.parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)


class TransactionAnalyser(object):
    """
    This class is used to analyse transactions of an address.
    It has methods that allows to perform on chain analysis of an address.
    """

    def __init__(self, df_transactions, df_address):

        self.df_transactions = df_transactions
        # holds a df of address/seed wallet we don't have to create it each time
        self.df_seed_wallet_naive = None
        self.df_seed_wallet = None
        self.gb_EOA_sorted = None
        self.df_address = df_address
        # We use a df address we can load all transactions in memory and then change the address list easily
        # for example to calculate on a specific project

        # store the array of string transactions
        self.dict_add_string_tx = None
        self.dict_add_value_string_tx = None

    def has_same_seed_naive(self, address):

        if self.df_seed_wallet_naive is None:
            self.set_seed_wallet_naive()
        df_same_seed = self.get_address_same_seed(self.df_seed_wallet_naive, address)
        return df_same_seed.shape[0] > 0

    def has_same_seed(self, address):

        if self.df_seed_wallet is None:
            self.set_seed_wallet()
        if address in self.df_seed_wallet.to_address.values:
            df_same_seed = self.get_address_same_seed(self.df_seed_wallet, address)
            return df_same_seed.shape[0] > 0
        else:
            return False

    @staticmethod
    def get_address_same_seed(df, address):

        seed_add = df.loc[address, 'from_address']
        df_same_seed = df.drop(address, axis=0).loc[
            df.drop(address, axis=0)['from_address'] == seed_add]
        return df_same_seed

    def has_suspicious_seed_behavior(self, address):

        return self.has_same_seed(address) != self.has_same_seed_naive(address)

    def set_seed_wallet_naive(self):

        if self.gb_EOA_sorted is None:
            self.set_group_by_sorted_EOA()
        self.df_seed_wallet_naive = self.gb_EOA_sorted.first().loc[:, ['from_address', 'to_address']]

    def set_seed_wallet(self):

        df_filtered = self.df_transactions[self.df_transactions['EOA'] == self.df_transactions['to_address']]
        df_gb = df_filtered.sort_values('block_timestamp', ascending=True).groupby('EOA')
        self.df_seed_wallet = df_gb.first().loc[:, ['from_address', 'to_address']]

    def set_group_by_sorted_EOA(self):

        if self.gb_EOA_sorted is None:
            self.gb_EOA_sorted = self.df_transactions.sort_values('block_timestamp', ascending=True).groupby('EOA')

    def has_less_than_n_transactions(self, address, n=5):

        self.set_group_by_sorted_EOA()
        return self.gb_EOA_sorted.get_group(address).shape[0] < n

    def has_interacted_with_other_contributor(self, address):

        self.set_group_by_sorted_EOA()
        contributors = self.get_contributors()
        other_contributors = contributors[contributors != address]

        df = self.gb_EOA_sorted.get_group(address)
        add_interacted = np.append(df['to_address'].to_numpy(), df['from_address'].to_numpy())
        add_interacted = add_interacted.astype('str')
        unique_add_interacted = np.unique(add_interacted)
        unique_add_interacted = unique_add_interacted[unique_add_interacted != address]
        return np.isin(unique_add_interacted, other_contributors).any()

    def get_contributors(self):

        return self.df_transactions['EOA'].unique()

    def transaction_similitude_pylcs(self, address, algo_type="address_only", minimum_sim_tx=5):

        # Transform all transactions into a 1D string
        if algo_type == "address_only":
            if self.dict_add_string_tx is None:
                self.set_dict_add_string_transactions(algo_type)
            str_transactions_target = self.dict_add_string_tx.get(address)
        elif algo_type == "address_and_value":
            if self.dict_add_value_string_tx is None:
                self.set_dict_add_string_transactions(algo_type)
            # Get all the transactions of the address in a 1D array
            str_transactions_target = self.dict_add_value_string_tx.get(address)
        else:
            Exception("algo_type not supported")

        shape_target = self.get_address_transactions(address).shape[0]
        min_shape = max(1, shape_target / 4)
        max_shape = max(shape_target, shape_target * 3)

        if self.df_address.columns != ['address']:
            self.df_address.columns = ['address']
        list_lcs = []
        for add in self.df_address['address']:
            if add != address:
                shape_other = self.get_address_transactions(add).shape[0]
                if min_shape < shape_other < max_shape:  # Heuristic to avoid comparing addresses with too different shapes
                    if algo_type == "address_only":
                        str_transactions_other = self.dict_add_string_tx.get(add)
                    else:
                        str_transactions_other = self.dict_add_value_string_tx.get(add)
                    lcs = self.longest_common_sub_string_pylcs(str_transactions_target, str_transactions_other)
                    list_lcs.append(lcs)
                else:
                    list_lcs.append(0)
            else:
                list_lcs.append(0)

        if minimum_sim_tx == -1:
            mask = np.array(list_lcs) > max(3, min(10, shape_target / 4))
        else:
            mask = np.array(list_lcs) > minimum_sim_tx
        df_similar_address = self.df_address.loc[mask, :].copy()
        df_similar_address['lcs'] = np.array(list_lcs)[mask]
        len_tx = len(str_transactions_target) / 2  # Divide by 2 because we have from_address and to_address
        df_similar_address['score'] = df_similar_address.loc[:, 'lcs'].apply(
            lambda x: min(x / len_tx, 1))
        return df_similar_address.set_index('address')

    @staticmethod
    def get_array_transactions(df_address_transactions, address, algo_type="address_only"):

        df_address_transactions.sort_values('block_timestamp', ascending=True, inplace=True)
        if algo_type == "address_only":
            try:
                array_transactions = df_address_transactions.loc[:, ['from_address', 'to_address']].dropna() \
                    .apply(lambda x: x.str[:8]) \
                    .replace(address[:8], 'x') \
                    .agg('-'.join, axis=1) \
                    .values
            except Exception as e:
                array_transactions = []
        elif algo_type == "address_and_value":
            try:
                array_transactions = df_address_transactions.loc[:, ['from_address', 'value', 'to_address']].dropna() \
                    .apply(lambda x: x.str[:8]) \
                    .replace(address, 'x') \
                    .agg('-'.join, axis=1) \
                    .values
            except Exception as e:
                array_transactions = []
        else:
            raise ValueError("algo_type must be either address_only or address_and_value")
        return array_transactions

    def get_address_transactions(self, address):

        try:
            df = self.gb_EOA_sorted.get_group(address)
        except Exception as e:
            if self.gb_EOA_sorted is None:
                self.set_group_by_sorted_EOA()
                df = self.get_address_transactions(address)
            else:
                df = pd.DataFrame()
        return df

    def get_address_transactions_add(self, df, address):

        return df[self.df_transactions['EOA'] == address]

    def set_dict_add_string_transactions(self, algo_type="address_only"):

        if self.gb_EOA_sorted is None:
            gb_address = self.df_transactions.groupby('EOA')
        else:
            gb_address = self.gb_EOA_sorted

        if algo_type == "address_only":
            if self.dict_add_string_tx is None:
                self.dict_add_string_tx = self.get_dict_string_tx(gb_address, algo_type=algo_type)
        elif algo_type == "address_and_value":
            if self.dict_add_value_string_tx is None:
                self.dict_add_value_string_tx = self.get_dict_string_tx(gb_address, algo_type=algo_type)
        else:
            raise ValueError("algo_type must be either address_only or address_and_value")

    def get_dict_string_tx(self, gb_address, algo_type="address_only"):
        dict_string_tx = {}
        for address, df_address in gb_address:
            array_transactions = self.get_array_transactions(df_address, address, algo_type)
            dict_string_tx[address] = "".join(array_transactions)
        return dict_string_tx

    @staticmethod
    def longest_common_sub_string_pylcs(string_target, string_other):

        # 1 similar transaction equals to 8 first char of the address + "-" + "x" = 10 char
        lcs = pylcs.lcs_string_length(string_target, string_other)
        return lcs // 10  # quotient of the division

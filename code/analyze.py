import config
import logging
from utils import Stats
import csv


class Analyzer:
    def __init__(self, context):
        self.context = context

    def execute(self):
        self.create_block_csv()
        self.create_tx_csv()
        self.create_tx_exceptions_csv()
        self.create_mempool_snapshots_csv()

        logging.info('Executed analyzer')

    def create_block_csv(self):
        with open(config.blocks_csv, 'w') as file:
            w = csv.writer(file, delimiter=';')
            w.writerow(['block_hash', 'node', 'timestamp', 'stale', 'height', 'total_size', 'txs',
                       'total_received', 'median_propagation', 'std_propagation'])
            for block in self.context.parsed_blocks.values():

                propagation_stats = Stats.from_array(block.receiving_timestamps)

                stale = True
                if block.block_hash in self.context.consensus_chain:
                    stale = False

                w.writerow([block.block_hash, block.node, block.timestamp, stale, block.height, block.total_size,
                                 block.txs, propagation_stats.count, propagation_stats.median, propagation_stats.std])

    def create_tx_csv(self):
        with open(config.txs_csv, 'w') as file:
            w = csv.writer(file, delimiter=';')
            w.writerow(['tx_hash', 'node', 'timestamp', 'total_accepted', 'median_propagation', 'std_propagation'])

            for tx in self.context.parsed_txs.values():
                propagation_stats = Stats.from_array(tx.receiving_timestamps)

                w.writerow([tx.tx_hash, tx.node, tx.timestamp,
                                propagation_stats.count, propagation_stats.median, propagation_stats.std])

    def create_tx_exceptions_csv(self):
        with open(config.tx_exceptions_csv, 'w') as file:
            w = csv.writer(file, delimiter=';')
            w.writerow(['node', 'timestamp', 'error_message'])

            for exce in self.context.tx_exceptions:
                w.writerow([exce.node, exce.timestamp, exce.error_message])

    def create_mempool_snapshots_csv(self):
        with open(config.mempool_snapshots_csv, 'w') as file:
            w = csv.writer(file, delimiter=';')
            w.writerow(['timestamp', 'node', 'txs', 'inputs'])

            for snapshot in self.context.mempool_snapshots:
                w.writerow([snapshot.timestamp, snapshot.node, snapshot.txs, snapshot.inputs])

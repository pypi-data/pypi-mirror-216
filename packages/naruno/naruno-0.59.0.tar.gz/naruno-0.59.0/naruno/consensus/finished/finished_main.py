#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import shutil
import time

from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.blocks_hash import GetBlockshash
from naruno.blockchain.block.blocks_hash import GetBlockshash_part
from naruno.blockchain.block.blocks_hash import SaveBlockshash
from naruno.blockchain.block.blocks_hash import SaveBlockshash_part
from naruno.blockchain.block.save_block import SaveBlock
from naruno.blockchain.block.save_block_to_blockchain_db import \
    SaveBlockstoBlockchainDB
from naruno.config import BLOCKS_PATH
from naruno.config import TEMP_ACCOUNTS_PATH
from naruno.config import TEMP_BLOCK_PATH
from naruno.config import TEMP_BLOCKSHASH_PART_PATH
from naruno.config import TEMP_BLOCKSHASH_PATH
from naruno.consensus.finished.transactions.transactions_main import \
    transactions_main
from naruno.consensus.finished.true_time.true_time_main import true_time
from naruno.lib.log import get_logger
from naruno.lib.mix.merkle_root import MerkleTree
from naruno.lib.settings_system import save_settings
from naruno.lib.settings_system import the_settings
from naruno.node.server.server import server
from naruno.transactions.pending_to_validating import PendingtoValidating

logger = get_logger("CONSENSUS")


def finished_main(
    block: Block,
    custom_TEMP_BLOCK_PATH: str = None,
    custom_BLOCKS_PATH: str = None,
    custom_TEMP_ACCOUNTS_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PART_PATH: str = None,
    custom_server: server = None,
    pass_sync: bool = False,
    dont_clean=False,
) -> None:
    the_server = None
    if custom_server is None:
        the_server = server.Server
    else:
        the_server = custom_server

    the_BLOCKS_PATH = BLOCKS_PATH if custom_BLOCKS_PATH is None else custom_BLOCKS_PATH
    the_TEMP_ACCOUNTS_PATH = (TEMP_ACCOUNTS_PATH if custom_TEMP_ACCOUNTS_PATH
                              is None else custom_TEMP_ACCOUNTS_PATH)
    the_TEMP_BLOCKSHASH_PATH = (TEMP_BLOCKSHASH_PATH
                                if custom_TEMP_BLOCKSHASH_PATH is None else
                                custom_TEMP_BLOCKSHASH_PATH)
    the_TEMP_BLOCKSHASH_PART_PATH = (TEMP_BLOCKSHASH_PART_PATH if
                                     custom_TEMP_BLOCKSHASH_PART_PATH is None
                                     else custom_TEMP_BLOCKSHASH_PART_PATH)

    the_TEMP_BLOCK_PATH = (TEMP_BLOCK_PATH if custom_TEMP_BLOCK_PATH is None
                           else custom_TEMP_BLOCK_PATH)
    block.sync_empty_blocks() if pass_sync is False else None
    if true_time(block):
        logger.debug(
            "Consensus proccess is complated, the block will be reset")

        reset_block = block.reset_the_block()

        settings = the_settings()
        if reset_block != False:
            block2 = reset_block[0]

            new_tx_from_us = False
            new_transactions_list = transactions_main(block2)
            if new_transactions_list is not None:
                SaveBlockstoBlockchainDB(
                    block2,
                    custom_BLOCKS_PATH=the_BLOCKS_PATH,
                    custom_TEMP_ACCOUNTS_PATH=the_TEMP_ACCOUNTS_PATH,
                    custom_TEMP_BLOCKSHASH_PATH=the_TEMP_BLOCKSHASH_PATH,
                    custom_TEMP_BLOCKSHASH_PART_PATH=
                    the_TEMP_BLOCKSHASH_PART_PATH,
                    dont_clean=dont_clean,
                )
                new_tx_from_us = True
                settings["save_blockshash"] = True
                save_settings(settings)
            if block2.sequence_number == 0:
                SaveBlockstoBlockchainDB(
                    block2,
                    custom_BLOCKS_PATH=the_BLOCKS_PATH,
                    custom_TEMP_ACCOUNTS_PATH=the_TEMP_ACCOUNTS_PATH,
                    custom_TEMP_BLOCKSHASH_PATH=the_TEMP_BLOCKSHASH_PATH,
                    custom_TEMP_BLOCKSHASH_PART_PATH=
                    the_TEMP_BLOCKSHASH_PART_PATH,
                    force=True,
                    dont_clean=dont_clean,
                )

            SaveBlockshash(
                reset_block[1].previous_hash,
                custom_TEMP_BLOCKSHASH_PATH=the_TEMP_BLOCKSHASH_PATH,
            )

            the_blocks_hash = GetBlockshash(
                custom_TEMP_BLOCKSHASH_PATH=the_TEMP_BLOCKSHASH_PATH)

            if len(the_blocks_hash) == block.part_amount:
                block.empty_block_number += block.gap_block_number

                block.sync = True
                SaveBlockshash_part(
                    MerkleTree(the_blocks_hash).getRootHash(),
                    custom_TEMP_BLOCKSHASH_PART_PATH=
                    the_TEMP_BLOCKSHASH_PART_PATH,
                )
                the_blockshas_part = GetBlockshash_part(
                    custom_TEMP_BLOCKSHASH_PART_PATH=
                    the_TEMP_BLOCKSHASH_PART_PATH)
                block.part_amount_cache = MerkleTree(
                    the_blockshas_part).getRootHash()
                if settings["save_blockshash"] == True:
                    shutil.copyfile(
                        the_TEMP_BLOCKSHASH_PATH,
                        (the_BLOCKS_PATH + str(block.sequence_number) +
                         ".blockshash_full.json"),
                    )
                    if not new_tx_from_us:
                        settings["save_blockshash"] = False
                        save_settings(settings)
                elif block.sequence_number - 1 == block.part_amount:
                    shutil.copyfile(
                        the_TEMP_BLOCKSHASH_PATH,
                        (the_BLOCKS_PATH + str(block.sequence_number) +
                         ".blockshash_full.json"),
                    )
                os.remove(the_TEMP_BLOCKSHASH_PATH)

                difference = (block.start_time +
                              (block.hard_block_number *
                               block.block_time)) - int(time.time())
                time.sleep(difference)

        PendingtoValidating(block)
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=the_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=the_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=the_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=the_TEMP_BLOCKSHASH_PART_PATH,
        )
        return True
    else:
        if block.sync == True:
            block.sync = False
            SaveBlock(
                block,
                custom_TEMP_BLOCK_PATH=the_TEMP_BLOCK_PATH,
                custom_TEMP_ACCOUNTS_PATH=the_TEMP_ACCOUNTS_PATH,
                custom_TEMP_BLOCKSHASH_PATH=the_TEMP_BLOCKSHASH_PATH,
                custom_TEMP_BLOCKSHASH_PART_PATH=the_TEMP_BLOCKSHASH_PART_PATH,
            )
            [
                the_server.send_block_to_other_nodes(sync_client, sync=True)
                for sync_client in the_server.sync_clients
            ]
            the_server.sync_clients = []

        logger.debug(
            "Consensus proccess is complated, waiting for the true time")
        return False

BLOCK_NUM = 0
BLOCK_ID = 1


def _to_blocklist(recent_blocks):
    """Convert a dictionary of blocks and block nums as returned by /block to
    a list of tuples (block_num, block_id) sorted in ascending order."""

    sorted_blocks = []
    for block in recent_blocks:
        sorted_blocks.append((
            recent_blocks[block]['BlockNum'],
            block
        ))

    sorted_blocks.sort()

    return sorted_blocks


# TODO: Optimize
def _align_blocknums(all_block_lists):
    """Return a list of block lists where every list starts at the same block
    number and ends at the same block number"""

    # Create lists of all block nums
    all_block_num_lists = [
        [block[BLOCK_NUM] for block in block_list] for block_list in all_block_lists
    ]

    # Get the large block number from a list of all of the smallest 
    # block numbers in all block lists.
    max_min = max(block_num_list[0] for block_num_list in all_block_num_lists)
    max_max = max(block_num_list[-1] for block_num_list in all_block_num_lists)

    # Make sure all block lists have a common block number. If not, then we
    # can't determine when they diverge.
    for block_num_list in all_block_num_lists:
        if max_min not in block_num_list:
            return -1

    # Line up the start of all the lists on the same block num
    for block_list in all_block_lists:
        while len(block_list) > 0:
            if block_list[0][0] != max_min:
                block_list.remove(block_list[0]) 
            else:
                break

    min_len = min(len(block_list) for block_list in all_block_lists) 

    return [block_list[:min_len] for block_list in all_block_lists], max_max


def get(stats):
    all_block_lists = []
    for node in stats:
        try:
            all_block_lists.append(
                _to_blocklist(stats[node]['block_history']['blocks'])
            )
        except KeyError:
            print("Failed to get block history.")

    aligned_block_lists, max_block_num = _align_blocknums(all_block_lists) 

    return  max_block_num - _first_divergence(aligned_block_lists)


def _first_divergence(aligned_block_lists):
    for i in range(len(aligned_block_lists[0])):
        block_id = aligned_block_lists[0][i][BLOCK_ID]

        for j in range(1, len(aligned_block_lists)):
            id_0 = aligned_block_lists[0][i][BLOCK_ID] 
            id_j = aligned_block_lists[j][i][BLOCK_ID]
            # print('[%d]' % i, id_0, '?=', id_j)
            if id_0 != id_j:

                if i == 0:
                    return -1
                else:
                    return aligned_block_lists[0][i][BLOCK_NUM]

    return aligned_block_lists[0][-1][BLOCK_NUM]

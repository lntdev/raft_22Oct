import yaml
import sim.timeline
import monitor.divergence
import random


def test_timeline():
    with open("sim/data/test.yaml") as fd:
        timeline = yaml.load(fd.read())

    sim.timeline.run(timeline, {})


def test_divergence():
    block_ids1 = [c for c in "abkdefghij"]
    block_ids2 = [c for c in "klmnopqrst"]

    d1 = {c: {'BlockNum': block_ids1.index(c) + 10} for c in block_ids1}
    d2 = {c: {'BlockNum': block_ids2.index(c) + 12} for c in block_ids2}

    print(monitor.divergence.get({
        'all': {'blocks': {'total': len(block_ids2) + 12}},
        0: {
            'blocks': {
                'recent': d1,
            },
        },
        1: {
            'blocks': {
                'recent': d2
            }
        }
    }))


def main():
    # test_timeline()
    test_divergence()

main()

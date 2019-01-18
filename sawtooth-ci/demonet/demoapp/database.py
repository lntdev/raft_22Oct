import os
import yaml
import time
import sqlite3


DB_FILE = 'demodata.db'
HOME_DIR = os.path.expanduser("~")
DB_DIR = os.path.join(HOME_DIR, '.demoapp')
DB_PATH = os.path.join(DB_DIR, DB_FILE)


def create(reset=False):
    # Create directory if needed
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    exists = False
    if os.path.exists(DB_PATH):
        exists = True

    db = sqlite3.connect(DB_PATH)

    if reset:
        doit = input(
            "Warning! About to delete all data stored in {}! Are you sure? (y/N) "
        )
        try:
            if doit == "y":
                c = db.cursor()
                c.execute("DROP TABLE lr") 
                db.commit()
                c.close()
        except sqlite3.OperationalError:
            print("Could not delete data, may not have existed.")

    if not exists or reset:
        c = db.cursor()
        create_cmd = (
            "CREATE TABLE lr ("
            "timestamp float,"
            "network text,"
            "tag text,"
            "cpu text,"
            "memory text,"
            "blocks text,"
            "transactions text,"
            "divergence text,"
            "stats text)"
        )
        c.execute(create_cmd)
        db.commit()
        c.close()
        print("Created new sqlite3 database: {}".format(DB_PATH))


    return db


def get_dashboard(db, networks):
    dash = {}

    for network in networks:
        c = db.cursor()
        c.execute(
            'SELECT * FROM lr WHERE network=? ORDER BY timestamp DESC', (network, )
        )
        data = c.fetchone()
        c.close()

        dash[network] = _make_summary(data)

    return dash


def get_query(db, network, limit=10):
    print("Got {}".format(network))

    c = db.cursor()
    c.execute(
        'SELECT * FROM lr WHERE network=? ORDER BY timestamp DESC LIMIT ?',
        (network, limit)
    )
    data = c.fetchall()
    c.close()

    return [_make_summary(datum) for datum in data]


def post_log(db, data):
    try:
        message = yaml.load(data)
    except BaseException as exception:
        print(exception)
        print("Failed to load YAML data")

    astats = message['stats']['all']

    timestamp = time.time()
    network = message['network']
    tag = message['tag']
    cpu = astats['cpu']
    memory = astats['mem']
    blocks = astats['blocks']
    transactions = astats['transactions']
    divergence = astats['divergence']
    stats = yaml.dump(message['stats'])
    
    c = db.cursor()
    c.execute("INSERT INTO lr VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        timestamp,
        network,
        tag,
        cpu,
        memory,
        blocks,
        transactions, 
        divergence,
        stats
    ))
    db.commit()

    c.close()

    return network, tag


def export_tag(db, tag):
    c = db.cursor()
    try:
        c.execute(
            'SELECT * FROM lr WHERE tag=? ORDER BY timestamp', (tag,)
        )
    except BaseException as exception:
        print(exception)
        return ""
    data = c.fetchall()
    c.close()
    try:
        return "---\n".join(["timestamp: {}\n{}".format(datum[0], datum[-1]) for datum in data])
    except BaseException as exception:
        print(tag)
        print("Failed to join timestamps to data")
        print(exception)
        return ""


def list_tags(db):
    c = db.cursor()
    try:
        c.execute(
            'SELECT DISTINCT tag FROM lr ORDER BY tag'
        )
    except BaseException as exception:
        print(exception)
        return [] 
    data = c.fetchall()
    c.close()
    return [d[0] for d in data]
 

def _make_summary(data):
    try:
        timestamp, network, tag, cpu, memory, blocks, transactions, divergence, _ = data
        print(memory)

        return {
            'timestamp': time.asctime(time.localtime(timestamp)),
            'cpu': cpu,
            'mem': _human_readable_bytes(int(memory)),
            'blocks': blocks,
            'transactions': transactions,
            'divergence': divergence,
        }
    except BaseException as err:
        print(err)
        return {
            'timestamp': '?',
            'cpu': '?',
            'mem': '?',
            'transactions': '?',
            'blocks': '?',
            'divergence': '?',
        }


def _human_readable_bytes(qty):
    if qty > 1024**4:
        out = "TB"
    elif qty > 1024**3:
        out = "GB"
    elif qty > 1024**2:
        out = "MB"
    elif qty > 1024:
        out = "KB"
    else:
        out = "B"
    return "{:.2f} {}".format(_convert_byte_units(qty, "B", out), out)


def _convert_byte_units(qty, units_in, units_out):
     units = ['B', 'KB', 'MB', 'GB', 'TB']
     if not (units_in in units and units_out in units):
         raise LrException("Invalid unit conversion {} > {}".format(
             units_in, units_out))
     idx_in = units.index(units_in)
     idx_out = units.index(units_out)

     steps = idx_out - idx_in

     if steps >= 0:
         return qty / 1024**steps
     else:
         return qty * 1024**steps

import ccxt
from funcoin.coins.base.cron import load_month
from notesecret.secret import read_secret, write_secret

path_root = '/home/bingtao/workspace/tmp/funcoin/'

load_month(ccxt.okex(), tmp_path=path_root)

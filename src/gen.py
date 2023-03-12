import os, sys
from .utils import *
from .configuration import Configuration

def generate_(src, dest):
    
    writer = codecs.open(os.path.abspath(dest), 'w', encoding='utf-8')
    conll_data = read_conll(src)
    with tqdm.tqdm(total=len(conll_data), position=0, leave=True) as pbar:
        for i, sen in enumerate(conll_data):
            if is_projective([e.head for e in sen[1:]]):
                conf = Configuration(sen)
                while not conf.is_terminal_state():
                    act, l = conf.next_gold_action()
                    label = (act + ':' + l) if l else act
                    wf, pf,lf = conf.features()
                    writer.write(' '.join(wf) + ' ' + ' '.join(pf)  + ' ' + ' '.join(lf)+ ' ' + label + '\n')
                    conf.do(act, l)
            #if (i+1) % 100 == 0: sys.stdout.write(str(i+1) + '...')
	    pbar.update(1)
    writer.close()
    print('done')


if __name__ == "__main__":
	src = sys.argv[1]
	dest = sys.argv[2]
	generate_(src, dest)

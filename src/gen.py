import os, sys
from .utils import *
from .configuration import Configuration
import tqdm
import json

def generate_(src, dest):
    
    writer = codecs.open(os.path.abspath(dest), 'w', encoding='utf-8')
    conll_data = [e for e in read_conll(src)]
    results = []
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
	    results.append({
	    	"word_features": wf,
	    	"pos_features": pf,
	    	"label_features": lf,
	    	"arc_action": act,
	    	"arc_label": l,
		    
	    })
            pbar.update(1)
    writer.close()
    return json.dumps(results, indent=4)


if __name__ == "__main__":
	src = sys.argv[1]
	dest = sys.argv[2]
	generate_(src, dest)

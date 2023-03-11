import os, sys
from collections import defaultdict
from .utils import *

def generate_vocab_files(src, dest):
	word_vocab = defaultdict(int)
	pos_vocab = set()
	pos_vocab.add('<null>')
	pos_vocab.add('<root>')
	label_vocab = set()
	label_vocab.add('<null>')


	for i, sen in enumerate(read_conll(os.path.abspath(src))):
		if is_projective([e.head for e in sen[1:]]):
			for e in sen:
				word_vocab[e.form]+=1
				pos_vocab.add(e.pos)
				label_vocab.add(e.relation)


	wv = dict()
	wv['<unk>'] = 0
	wv['<null>'] = 1
	wv['<root>'] = 2

	for w in word_vocab.keys():
		if (word_vocab[w]>1) and not (w in wv):
			wv[w] = len(wv)

	pv = dict()
	for p in pos_vocab:
		if not (p in pv):
			pv[p] = len(pv)


	result = {}
# 	w_vocab_writer = codecs.open(os.path.abspath(dest)+'.word','w',encoding='utf8')
# 	for w in wv.keys():
# 		w_vocab_writer.write(w+' '+str(wv[w])+'\n')
# 	w_vocab_writer.close()
	
	result['words'] = wv

# 	p_vocab_writer = codecs.open(os.path.abspath(dest)+'.pos','w',encoding='utf8')
# 	for i, p in enumerate(pos_vocab):
# 		p_vocab_writer.write(p+' '+str(i)+'\n')
# 	p_vocab_writer.close()
	
	result['pos'] = {p: i for i, p in enumerate(pos_vocab)}

# 	l_vocab_writer = codecs.open(os.path.abspath(dest)+'.labels','w',encoding='utf8')
# 	for i, d in enumerate(label_vocab):
# 		l_vocab_writer.write(d+' '+str(i)+'\n')
# 	l_vocab_writer.close()
	
	result['labels'] = {l: i for i, l in enumerate(label_vocab)}

# 	a_vocab_writer = codecs.open(os.path.abspath(dest)+'.actions','w',encoding='utf8')
# 	a_vocab_writer.write('SHIFT'+' 0' +'\n')
# 	for i, d in enumerate(label_vocab):
# 		a_vocab_writer.write('LEFT-ARC:'+d+' '+str(i+1)+'\n')
# 	for i, d in enumerate(label_vocab):
# 		a_vocab_writer.write('RIGHT-ARC:'+d+' '+str(i+1+len(label_vocab))+'\n')

# 	a_vocab_writer.close()

	actionlist = ['SHIFT']
	actionlist += ['LEFT-ARC:'+d for d in label_vocab]
	actionlist += ['RIGHT-ARC:'+d for d in label_vocab]
	
	result['actions'] = {a: i for i, a in enumerate(actionlist)}
	
	return result
	
	
if __name__ == "__main__":
	src = sys.argv[1]
	dest = sys.argv[2]
	generate_vocab_files(src, dest)

from gensim import corpora, models, similarities

bb_corpus = 'bb_spoilers.txt'

def load_corpus(corpora):
	# Accepts a list of filenames containing spoilers
	corpus = []
	for filename in corpora:
		with open(filename) as f:
			lines = f.read().splitlines()
			corpus += lines
	return corpus

def main():
	corpus = load_corpus([bb_corpus])
	tfidf = models.TfidfModel(corpus)


if __name__ == '__main__':
	main()
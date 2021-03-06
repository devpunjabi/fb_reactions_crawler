import argparse
import operator
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize.moses import MosesDetokenizer


def parse_arguments():
    parser = argparse.ArgumentParser(description='Normalize crawled and filtered facebook reactions.')
    parser.add_argument('filename', metavar='filename', help='a filtered json file')
    return parser.parse_args()


def get_most_common_reaction(reactions):
    reaction = max(reactions.items(), key=operator.itemgetter(1))[0]
    if reaction == 'angry':
        return 'anger'
    elif reaction == 'haha':
        return 'joy'
    elif reaction == 'love':
        return 'joy'
    elif reaction == 'sad':
        return 'sadness'
    elif reaction == 'wow':
        return 'surprise'
    print('wrong')
    return None



def normalize(post):
    reaction = get_most_common_reaction(post['reactions'])
    message = word_tokenize(post['message'])
    sw = stopwords.words('english')

    words_without_stopwords = [word for word in message if word not in sw]

    detokenizer = MosesDetokenizer()
    message_without_stopwords = detokenizer.detokenize(words_without_stopwords, return_str=True)

    return {'message': message_without_stopwords, 'reaction': reaction}

def normalize_data(filename):
    posts = None
    with open(filename, 'r') as infile:
        posts = json.load(infile)

    normalized_posts = list(map(normalize, posts))
    filename = filename.strip('.json') + '_normalized.json'
    with open(filename, 'w') as outfile:
        json.dump(normalized_posts, outfile)
    return filename

def main(run_args):
    normalize_data(run_args.filename)    


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

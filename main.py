import argparse
from train_and_test import train_and_test
from parameters import dataset_parameters_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-pos_fa", "--positive_fasta", action="store", dest='pos_fa', required=True,
                        help="positive fasta file")
    parser.add_argument("-neg_fa", "--negative_fasta", action="store", dest='neg_fa', required=True,
                        help="negative fasta file")
    parser.add_argument("-test_fa", "--test_fasta", action="store", dest='test_fa', required=True,
                        help="test fasta  file")
    parser.add_argument("-dataset", "--dataset_name", action="store", dest='dataset', required=True,
                        help="the name of dataset, such as A101")
    parser.add_argument("-out_path", "--out_path", action="store", dest='out_path', required=True,
                        help="The path to save the prediction results")
    parser.add_argument("-save_path", "--save_path", action="store", dest='save_path', required=False, default=None,
                        help="The path to save the features of training dataset and test dataset.")

    args = parser.parse_args()
    pos_train_fa = args.pos_fa
    neg_train_fa = args.neg_fa
    test_fa = args.test_fa
    dataset = args.dataset
    if dataset not in dataset_parameters_dict.keys():
        print("Error!")
    out = args.out_path
    save_path = args.save_path
    print(pos_train_fa, neg_train_fa, test_fa, dataset, out, save_path)
    train_and_test(pos_train_fa, neg_train_fa, test_fa, dataset, out, save_path=save_path)


if __name__ == "__main__":
    main()

cpm_dict = {'A': (1., 1., 1.), 'C': (0., 0., 1.), 'G': (1., 0., 0.), 'U': (0., 1., 0.)}
cpm_dict2 = {'A': [0., 0., 0., 1.], 'C': [0., 0., 1., 0.], 'G': [0., 1., 0., 0.], 'U': [1., 0., 0., 0.]}
seq_dict = {'A': 0, 'C': 1, 'G': 2, 'U': 3}


def density(seq):
    res = []
    d = {'A': 0., 'U': 0., 'C': 0., 'G': 0.}
    for i in range(len(seq)):
        d[seq[i]] += 1
        res.append(d[seq[i]] / (i + 1))
    return res


def get_NCP_ND_feature(seq):
    res = []
    # seq = remove_center_GAC(seq)
    den = density(seq)
    for n, i in zip(seq, range(len(den))):
        res.extend(cpm_dict[n])
        res.append(den[i])
    return res


if __name__ == "__main__":
    seq = "CAAAGGACGUGAC"
    print(density(seq))
    print(get_NCP_ND_feature(seq))
    print(seq)

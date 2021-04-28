import pandas as pd


def get_RNAPhyche(phy_list=None, k=2, standardized=False):
    '''
    Get the physical and chemical properties values of RNA
    :param phy_list: the names of physical and chemical properties
    :param k:
    :param standardized: If it is True, then the ouput values is normalized.
    :return RNAPhyche:a DataFrame
    '''
    RNAPhyche = pd.DataFrame()
    if phy_list is None or phy_list == []:
        print("Use all the physical and chemical properties.")
    elif isinstance(phy_list, list):
        print("Use the physical and chemical properties " + str(phy_list))
    else:
        print("Error! Please input the correct phy_list.")

    if k == 2:
        nucleotide = ['A', 'C', 'G', 'U']
        dimer = [n1 + n2 for n1 in nucleotide for n2 in nucleotide]
        RNAPhyche['kmer'] = dimer
        RNAPhyche = RNAPhyche.set_index('kmer')

        RNAPhyche['Slide(RNA)'] = [-1.27, -1.43, -1.5, -1.36, -1.46, -1.78, -1.89, -1.5, -1.7, -1.39, -1.78, -1.43,
                                   -1.45, -1.7, -1.46, -1.27]
        RNAPhyche['Adenine_content'] = [2.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
        RNAPhyche['Hydrophilicity(RNA)'] = [0.04, 0.14, 0.08, 0.14, 0.21, 0.49, 0.35, 0.52, 0.1, 0.26, 0.17, 0.27, 0.21,
                                            0.48, 0.34, 0.44]
        RNAPhyche['Tilt(RNA)'] = [-0.8, 0.8, 0.5, 1.1, 1.0, 0.3, -0.1, 0.5, 1.3, 0.0, 0.3, 0.8, -0.2, 1.3, 1.0, -0.8]
        RNAPhyche['Stacking_energy(RNA)'] = [-13.7, -13.8, -14.0, -15.4, -14.4, -11.1, -15.6, -14.0, -14.2, -16.9,
                                             -11.1, -13.8, -16.0, -14.2, -14.4, -13.7]
        RNAPhyche['Twist(RNA)'] = [31.0, 32.0, 30.0, 33.0, 31.0, 32.0, 27.0, 30.0, 32.0, 35.0, 32.0, 32.0, 32.0, 32.0,
                                   31.0, 31.0]
        RNAPhyche['Entropy(RNA)'] = [-18.4, -26.2, -19.2, -15.5, -27.8, -29.7, -19.4, -19.2, -35.5, -34.9, -29.7, -26.2,
                                     -22.6, -26.2, -19.2, -18.4]
        RNAPhyche['Roll(RNA)'] = [7.0, 4.8, 8.5, 7.1, 9.9, 8.7, 12.1, 8.5, 9.4, 6.1, 12.1, 4.8, 10.7, 9.4, 9.9, 7.0]
        RNAPhyche['Purine(AG)_content'] = [2.0, 1.0, 2.0, 1.0, 1.0, 0.0, 1.0, 0.0, 2.0, 1.0, 2.0, 1.0, 1.0, 0.0, 1.0,
                                           0.0]
        RNAPhyche['Hydrophilicity(RNA)1'] = [0.023, 0.083, 0.035, 0.09, 0.11800000000000001, 0.349, 0.193,
                                             0.37799999999999995, 0.048, 0.146, 0.065, 0.16, 0.11199999999999999, 0.359,
                                             0.22399999999999998, 0.389]
        RNAPhyche['Enthalpy(RNA)1'] = [-6.82, -11.4, -10.48, -9.38, -10.44, -13.39, -10.64, -10.48, -12.44, -14.88,
                                       -13.39, -11.4, -7.69, -12.44, -10.44, -6.82]
        RNAPhyche['GC_content'] = [0.0, 1.0, 1.0, 0.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0, 0.0, 1.0, 1.0, 0.0]
        RNAPhyche['Entropy(RNA)1'] = [-19.0, -29.5, -27.1, -26.7, -26.9, -32.7, -26.7, -27.1, -32.5, -36.9, -32.7,
                                      -29.5, -20.5, -32.5, -26.9, -19.0]
        RNAPhyche['Rise(RNA)'] = [3.18, 3.24, 3.3, 3.24, 3.09, 3.32, 3.3, 3.3, 3.38, 3.22, 3.32, 3.24, 3.26, 3.38, 3.09,
                                  3.18]
        RNAPhyche['Free_energy(RNA)'] = [-0.9, -2.1, -1.7, -0.9, -1.8, -2.9, -2.0, -1.7, -2.3, -3.4, -2.9, -2.1, -1.1,
                                         -2.1, -1.7, -0.9]
        RNAPhyche['Keto(GT)_content'] = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 2.0]
        RNAPhyche['Free_energy(RNA)1'] = [-0.93, -2.24, -2.08, -1.1, -2.11, -3.26, -2.36, -2.08, -2.35, -3.42, -3.26,
                                          -2.24, -1.33, -2.35, -2.11, -0.93]
        RNAPhyche['Enthalpy(RNA)'] = [-6.6, -10.2, -7.6, -5.7, -10.5, -12.2, -8.0, -7.6, -13.3, -14.2, -12.2, -10.2,
                                      -8.1, -10.2, -7.6, -6.6]
        RNAPhyche['Guanine_content'] = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 2.0, 1.0, 0.0, 0.0, 1.0, 0.0]
        RNAPhyche['Shift(RNA)'] = [-0.08, 0.23, -0.04, -0.06, 0.11, -0.01, 0.3, -0.04, 0.07, 0.07, -0.01, 0.23, -0.02,
                                   0.07, 0.11, -0.08]
        RNAPhyche['Cytosine_content'] = [0.0, 1.0, 0.0, 0.0, 1.0, 2.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
        RNAPhyche['Thymine_content'] = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0]
        RNAPhyche['Base_stacking_energy'] = [1.30, 1.73, 1.51, 1.33, 1.10, 1.51, 1.20, 1.15, 2.07, 2.22, 1.37, 1.11,
                                             1.33, 0.85, 0.77, 1.75]
        RNAPhyche = RNAPhyche[phy_list]

    else:
        print("Error! Please input the correct value of k.")

    if standardized:
        for col in RNAPhyche.columns:
            RNAPhyche[col] = (RNAPhyche[col] - RNAPhyche[col].mean()) / RNAPhyche[col].std()
    return RNAPhyche


if __name__ == "__main__":
    # RNAPhyche = get_RNAPhyche(
    #     ['Rise(RNA)', 'Roll(RNA)', 'Shift(RNA)', 'Slide(RNA)', 'Tilt(RNA)', 'Twist(RNA)', 'Enthalpy(RNA)1',
    #      'Entropy(RNA)', 'Stacking_energy(RNA)', 'Free_energy(RNA)'], standardized=True)

    RNAPhyche = get_RNAPhyche(
        ['Rise(RNA)', 'Roll(RNA)', 'Shift(RNA)', 'Slide(RNA)', 'Tilt(RNA)', 'Twist(RNA)'], standardized=True)
    RNAPhyche = RNAPhyche.apply(lambda x: round(x, 3))

    RNAPhyche.to_csv("RNAPhyche.csv")

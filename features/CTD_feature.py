def get_CTD_feature(seq):
    n = float(len(seq) - 1)
    num_A, num_U, num_G, num_C = 0.0, 0.0, 0.0, 0.0
    AU_trans, AG_trans, AC_trans, UG_trans, UC_trans, GC_trans = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    for i in range(len(seq) - 1):
        if seq[i] == "A":
            num_A = num_A + 1
        if seq[i] == "U":
            num_U = num_U + 1
        if seq[i] == "G":
            num_G = num_G + 1
        if seq[i] == "C":
            num_C = num_C + 1
        if (seq[i] == "A" and seq[i + 1] == "U") or (seq[i] == "U" and seq[i + 1] == "A"):
            AU_trans = AU_trans + 1
        if (seq[i] == "A" and seq[i + 1] == "G") or (seq[i] == "G" and seq[i + 1] == "A"):
            AG_trans = AG_trans + 1
        if (seq[i] == "A" and seq[i + 1] == "C") or (seq[i] == "C" and seq[i + 1] == "A"):
            AC_trans = AC_trans + 1
        if (seq[i] == "U" and seq[i + 1] == "G") or (seq[i] == "G" and seq[i + 1] == "U"):
            UG_trans = UG_trans + 1
        if (seq[i] == "U" and seq[i + 1] == "C") or (seq[i] == "C" and seq[i + 1] == "U"):
            UC_trans = UC_trans + 1
        if (seq[i] == "G" and seq[i + 1] == "C") or (seq[i] == "C" and seq[i + 1] == "G"):
            GC_trans = GC_trans + 1

    a, u, g, c = 0, 0, 0, 0
    A0_dis, A1_dis, A2_dis, A3_dis, A4_dis = 0.0, 0.0, 0.0, 0.0, 0.0
    U0_dis, U1_dis, U2_dis, U3_dis, U4_dis = 0.0, 0.0, 0.0, 0.0, 0.0
    G0_dis, G1_dis, G2_dis, G3_dis, G4_dis = 0.0, 0.0, 0.0, 0.0, 0.0
    C0_dis, C1_dis, C2_dis, C3_dis, C4_dis = 0.0, 0.0, 0.0, 0.0, 0.0
    for i in range(len(seq) - 1):
        if seq[i] == "A":
            a = a + 1
            if a == 1:
                A0_dis = ((i * 1.0) + 1) / n
            if a == int(round(num_A / 4.0)):
                A1_dis = ((i * 1.0) + 1) / n
            if a == int(round(num_A / 2.0)):
                A2_dis = ((i * 1.0) + 1) / n
            if a == int(round((num_A * 3 / 4.0))):
                A3_dis = ((i * 1.0) + 1) / n
            if a == num_A:
                A4_dis = ((i * 1.0) + 1) / n
        if seq[i] == "U":
            u = u + 1
            if u == 1:
                U0_dis = ((i * 1.0) + 1) / n
            if u == int(round(num_U / 4.0)):
                U1_dis = ((i * 1.0) + 1) / n
            if u == int(round((num_U / 2.0))):
                U2_dis = ((i * 1.0) + 1) / n
            if u == int(round((num_U * 3 / 4.0))):
                U3_dis = ((i * 1.0) + 1) / n
            if u == num_U:
                U4_dis = ((i * 1.0) + 1) / n
        if seq[i] == "G":
            g = g + 1
            if g == 1:
                G0_dis = ((i * 1.0) + 1) / n
            if g == int(round(num_G / 4.0)):
                G1_dis = ((i * 1.0) + 1) / n
            if g == int(round(num_G / 2.0)):
                G2_dis = ((i * 1.0) + 1) / n
            if g == int(round(num_G * 3 / 4.0)):
                G3_dis = ((i * 1.0) + 1) / n
            if g == num_G:
                G4_dis = ((i * 1.0) + 1) / n
        if seq[i] == "C":
            c = c + 1
            if c == 1:
                C0_dis = ((i * 1.0) + 1) / n
            if c == int(round(num_C / 4.0)):
                C1_dis = ((i * 1.0) + 1) / n
            if c == int(round(num_C / 2.0)):
                C2_dis = ((i * 1.0) + 1) / n
            if c == int(round(num_C * 3 / 4.0)):
                C3_dis = ((i * 1.0) + 1) / n
            if c == num_C:
                C4_dis = ((i * 1.0) + 1) / n
    CTD_feature = [num_A / n, num_U / n, num_G / n, num_C / n,
                   AU_trans / n - 1, AG_trans / (n - 1), AC_trans / (n - 1),
                   UG_trans / n - 1, UC_trans / (n - 1), GC_trans / (n - 1),
                   A0_dis, A1_dis, A2_dis, A3_dis, A4_dis,
                   U0_dis, U1_dis, U2_dis, U3_dis, U4_dis,
                   G0_dis, G1_dis, G2_dis, G3_dis, G4_dis,
                   C0_dis, C1_dis, C2_dis, C3_dis, C4_dis]
    return CTD_feature

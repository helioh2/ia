

def scale_value(x, minimo, maximo):
    return (x - minimo) / (maximo - minimo)


def gen_gen_pertinence(func_values, lim=1.):

    # VL,L,M,H,VH = func_values

    def gen_pertinence_very_low(minimo, maximo):
        def pertinence_very_low(x, limite=lim):
            x = scale_value(x, minimo, maximo)
            VL = func_values[0]
            TOPO, BAIXO = VL
            if x <= TOPO:
                return limite
            elif TOPO < x <= BAIXO:
                pert = 1 - (x - TOPO) / (BAIXO - TOPO)
                return pert if pert < limite else limite
            else:
                return 0.

        return pertinence_very_low


    def gen_gen_pertinence_medium(i):
        def gen_pertinence_medium(minimo, maximo):
            def pertinence_medium(x, limite=lim):
                x = scale_value(x, minimo, maximo)
                M = func_values[i]
                BAIXO1, TOPO, BAIXO2 = M
                if BAIXO1 < x <= TOPO:
                    pert = (x - BAIXO1) / (TOPO - BAIXO1)
                    return pert if pert < limite else limite
                elif TOPO < x <= BAIXO2:
                    pert = 1 - ((x - TOPO) / (BAIXO2 - TOPO))
                    return pert if pert < limite else limite
                else:
                    return 0.

            return pertinence_medium

        return gen_pertinence_medium


    def gen_pertinence_very_high(minimo, maximo):
        def pertinence_very_high(x, limite=lim):
            x = scale_value(x, minimo, maximo)
            VH = func_values[-1]
            BAIXO, TOPO = VH
            if BAIXO < x <= TOPO:
                pert = (x - BAIXO) / (TOPO - BAIXO)
                return pert if pert < limite else limite
            elif x > TOPO:
                return limite
            else:
                return 0.

        return pertinence_very_high

    if len(func_values) < 2:
        return -1

    pert_functions = [gen_pertinence_very_low]
    for i in range(1, len(func_values)-1):
        pert_functions.append(gen_gen_pertinence_medium(i))
    pert_functions.append(gen_pertinence_very_high)
    return pert_functions

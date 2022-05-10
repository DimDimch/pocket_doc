from Naked.toolshed.shell import muterun_js


def dermatology_make_prediction(img_path):
    response = muterun_js('net.js', img_path)
    if response.exitcode == 0:
        standard_out = response.stdout.decode().split('!!!! ')[1].split(', ')
        standard_out = standard_out[:(len(standard_out) - 1)]

        # make out string
        prob1 = round(float(standard_out[1]), 2)
        if prob1 == 100:
            prob1 = '> 99.9'
        prob2 = round(float(standard_out[3]), 2)
        if prob2 == 0:
            prob2 = '< 0.1'
        prob3 = round(float(standard_out[5]), 2)
        if prob3 == 0:
            prob3 = '< 0.1'

        disease1 = str(standard_out[0]) + '- вероятность ' + str(prob1) + '%' + '\n'
        disease2 = str(standard_out[2]) + '- вероятность ' + str(prob2) + '%' + '\n'
        disease3 = str(standard_out[4]) + '- вероятность ' + str(prob3) + '%' + '\n'
        disease = 'Возможные заболевания:\n' + disease1 + disease2 + disease3
        return disease
    else:
        return 'Извините, возникла ошибка'


if __name__ == "__main__":
    disease = dermatology_make_prediction('ISIC_0024839.jpg')
    print(disease)

import numpy as np
from ..vietnamese_nlp.exe_backends.trt_loader import TrtOCREncoder, TrtOCRDecoder
from ..vietnamese_nlp.vietocr.tool.translate import translate_trt, process_input, \
    process_image
from ..vietnamese_nlp.vietocr.model.vocab import Vocab
from ..vietnamese_nlp.vietocr.tool.config import Cfg


configs = Cfg.load_config_from_name('vgg_transformer')
configs['pretrained'] = False
configs['device'] = 'cuda:0'


class TensorRuntimeOCR(object):
    def __init__(self, encoder_model, decoder_model, config=configs):
        self.encoder_model = TrtOCREncoder(encoder_model)
        self.encoder_model.build()
        self.decoder_model = TrtOCRDecoder(decoder_model)
        self.decoder_model.build()
        self.config = config
        self.vocab = Vocab(config['vocab'])

    def preprocess_batch(self, list_img):
        '''
            list_img: list of PIL Image
        '''
        total_img = len(list_img)
        # Get max shape
        batch_width = 0
        batch_list = []
        for idx, img in enumerate(list_img):
            img = process_image(img, self.config['dataset']['image_height'],
                                self.config['dataset']['image_min_width'], self.config['dataset']['image_max_width'])
            im_width = img.shape[2]
            if im_width > batch_width:
                batch_width = im_width
            batch_list.append(img)
            # Create batch
        batch = np.ones((total_img, 3, self.config['dataset']['image_height'], batch_width))
        for idx, single in enumerate(batch_list):
            _, height, width = single.shape
            batch[idx, :, :, :width] = single
        return batch

    def predict(self, img, return_prob=True):
        '''
            Predict single-line image
            Input:
                - img: pillow Image
        '''
        img = process_input(img, self.config['dataset']['image_height'],
                            self.config['dataset']['image_min_width'], self.config['dataset']['image_max_width'])

        s, prob = translate_trt(img, self.encoder_model, self.decoder_model)
        s = s[0].tolist()
        prob = prob[0]

        s = self.vocab.decode(s)
        if return_prob:
            return s, prob
        else:
            return s

    def predict_batch(self, list_img, return_prob=True):
        '''
            Predict batch of image
            Input:
                - img: pillow Image
        '''
        # Preprocess
        batch = self.preprocess_batch(list_img)
        # Feed to CNN + transformer
        translated_sentence, prob = translate_trt(batch, self.encoder_model, self.decoder_model)
        # Decode result
        result = []
        for i, s in enumerate(translated_sentence):
            s = translated_sentence[i].tolist()
            s = self.vocab.decode(s)
            result.append((s, prob[i]))

        return result


if __name__ == '__main__':
    pass
    # config = Cfg.load_config_from_name('vgg_transformer')
    # dataset_params = {
    #     'name': 'hw',
    #     'data_root': './my_data/',
    #     'train_annotation': 'train_line_annotation.txt',
    #     'valid_annotation': 'test_line_annotation.txt'
    # }
    #
    # params = {
    #     'print_every': 200,
    #     'valid_every': 15 * 200,
    #     'iters': 20000,
    #     'checkpoint': './checkpoint/transformerocr_checkpoint.pth',
    #     'export': './weights/transformerocr.pth',
    #     'metrics': 10000
    # }
    #
    # config['trainer'].update(params)
    # config['dataset'].update(dataset_params)
    # config['device'] = 'cuda:0'
    #
    # img1 = Image.open('image/test.png')
    # img2 = Image.open('image/test_2.png')
    # img3 = Image.open('image/test_3.png')
    # # Trt
    # ocr_model = TensorRuntimeOCR('transformer_encoder.trt', 'transformer_decoder.trt', config)
    # print(ocr_model.predict_batch([img1, img2, img3]))

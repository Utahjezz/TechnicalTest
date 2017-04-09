package it.technicaltest.service.impl;

import it.technicaltest.service.ImageCustomClassifier;
import okhttp3.MultipartBody;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;

/**
 * Created by giacomogezzi on 08/04/17.
 */
@Service
public class ImageCustomClassifierImpl implements ImageCustomClassifier {

    @PostConstruct
    public void init() {
        MultipartBody.Builder bodyBuilder = new MultipartBody.Builder().setType(MultipartBody.FORM);
        bodyBuilder.addFormDataPart(PARAM_NAME, options.classifierName());
    }

    @Override
    public void trainClassifier() {

    }

    @Override
    public void classify() {

    }
}

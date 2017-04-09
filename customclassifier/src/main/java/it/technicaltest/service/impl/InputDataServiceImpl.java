package it.technicaltest.service.impl;

import it.technicaltest.domain.ClassifierInputOptions;
import it.technicaltest.service.InputDataService;
import org.springframework.stereotype.Service;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by giacomogezzi on 08/04/17.
 */
@Service
public class InputDataServiceImpl implements InputDataService{

    @Override
    public ClassifierInputOptions prepareClassifierInputOptions(String inputFileBaseDir) {
        ClassifierInputOptions classifierInputOptions = new ClassifierInputOptions();
        File baseDir = new File(inputFileBaseDir);
        Map<String, String> inputData = new HashMap<>();
        for (File file : baseDir.listFiles()) {
            if (file.isDirectory()) {

            } else {
                inputData.put(file.getName().replace("-","_").replace(".zip", ""), file.getAbsolutePath());
            }
        }
        classifierInputOptions.setTrainingSet(inputData);
        return classifierInputOptions;
    }
}

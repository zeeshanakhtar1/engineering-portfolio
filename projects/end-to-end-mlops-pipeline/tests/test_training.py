import tempfile,unittest
from pathlib import Path
from mlops.train import train,train_from_csv
from mlops.predict import predict

class PipelineTests(unittest.TestCase):
    def test_linear_model(self):
        rows=[{'x':str(x),'y':str(2*x+1)} for x in range(1,11)]
        model=train(rows)
        self.assertAlmostEqual(model['weights']['x'],2)
        self.assertAlmostEqual(model['weights']['intercept'],1)
        self.assertAlmostEqual(model['evaluation']['mae'],0)
    def test_artifact_and_inference(self):
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/'dataset.csv'
            src.write_text('x,y\n'+'\n'.join(f'{x},{2*x+1}' for x in range(1,11)))
            dest=Path(d)/'model.json'
            artifact=train_from_csv(src,dest)
            self.assertTrue(dest.exists())
            self.assertEqual(len(artifact['training_data_sha256']),64)
            self.assertAlmostEqual(predict(dest,12),25)
    def test_insufficient_rows(self):
        with self.assertRaises(ValueError):train([{'x':'1','y':'2'}])
    def test_feature_variance(self):
        with self.assertRaises(ValueError):train([{'x':'2','y':str(x)} for x in range(10)])
if __name__=='__main__':unittest.main()

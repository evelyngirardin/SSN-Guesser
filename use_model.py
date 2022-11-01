from model_building import LitClassifier
from model_building import DMFDataset
import torch

# The list of states in the lookup table.
#['AK' 'AL' 'AR' 'AZ' 'CA' 'CO' 'CT' 'DC' 'DE' 'FL' 'GA' 'HI' 'IA' 'ID'
#'IL' 'IN' 'KS' 'KY' 'LA' 'MA' 'MD' 'ME' 'MI' 'MN' 'MO' 'MS' 'MT' 'NC'
#'ND' 'NE' 'NH' 'NJ' 'NM' 'NV' 'NY' 'OH' 'OK' 'OR' 'PA' 'RI' 'SC' 'SD'
#'TN' 'TX' 'UT' 'VA' 'VI,PR' 'VT' 'WA' 'WI' 'WV' 'WV,NC' 'WY']

model = LitClassifier()
model.load_state_dict(torch.load("model1"))

with torch.no_grad():
    model.eval()
    print(model)
    test = [1960, 5, 24, 4]
    test = torch.Tensor(test)
    print(model(test))

model.train()
import torch.nn as nn

class PoseLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=51, hidden_size=128, num_layers=2, batch_first=True, dropout=0.3)
        self.fc = nn.Linear(128, 4)

    def forward(self, x):
        _, (h, _) = self.lstm(x)
        return self.fc(h[-1])
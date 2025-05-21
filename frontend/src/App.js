import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Grid,
  CircularProgress,
  Alert,
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CodeReviewResults from './components/CodeReviewResults';
import MetricsDashboard from './components/MetricsDashboard';
import { reviewCode } from './services/api';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [reviewResults, setReviewResults] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const results = await reviewCode(code, language);
      setReviewResults(results);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            AI Code Review Assistant
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <form onSubmit={handleSubmit}>
                  <TextField
                    fullWidth
                    multiline
                    rows={10}
                    variant="outlined"
                    label="Enter your code"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    select
                    label="Programming Language"
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    margin="normal"
                    SelectProps={{
                      native: true,
                    }}
                  >
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="java">Java</option>
                    <option value="cpp">C++</option>
                  </TextField>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    fullWidth
                    disabled={loading}
                    sx={{ mt: 2 }}
                  >
                    {loading ? <CircularProgress size={24} /> : 'Review Code'}
                  </Button>
                </form>
              </Paper>
            </Grid>

            <Grid item xs={12} md={6}>
              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}
              {reviewResults && (
                <CodeReviewResults results={reviewResults} />
              )}
            </Grid>
          </Grid>

          {reviewResults && (
            <Box sx={{ mt: 4 }}>
              <MetricsDashboard results={reviewResults} />
            </Box>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 
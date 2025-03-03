import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Rankings from './components/Rankings';
import Vote from './components/Vote';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Rankings />} />
          <Route path="vote" element={<Vote />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;

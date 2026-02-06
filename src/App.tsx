import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import { Login } from './login';

export default function App() {
    return (
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
        </Routes>
      </Router>
    );
  }
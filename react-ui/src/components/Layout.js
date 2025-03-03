import React from 'react';
import { Outlet, Link } from 'react-router-dom';

function Layout() {
  return (
    <>
      <nav className="bg-white shadow-lg">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex justify-between">
            <div className="flex space-x-7">
              <div>
                <Link to="/" className="flex items-center py-4">
                  <span className="font-semibold text-gray-500 text-lg">Billionaire Impact Rankings</span>
                </Link>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Link to="/vote" className="py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white rounded-lg">Vote</Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>

      <footer className="bg-white shadow-lg mt-8">
        <div className="container mx-auto px-4 py-6 text-center text-gray-600">
          <p>Data sourced from OpenSecrets, ProPublica, CDP, SEC, and Glassdoor</p>
        </div>
      </footer>
    </>
  );
}

export default Layout;

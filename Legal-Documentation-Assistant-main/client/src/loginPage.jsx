import React from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const redirectToSignup = () => {
    navigate("/signup");
  };

  const handleLogin = async (event) => {
    event.preventDefault(); // Prevent default form submission
    const email = event.target.email.value;
    const password = event.target.password.value;

    const response = await fetch("http://localhost:5000/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      navigate("/"); // Redirect to home page after successful login
    } else {
      const data = await response.json();
      alert(data.message || "Login failed. Please try again."); // Display error message
    }
    event.preventDefault(); // Prevent default form submission

    // TODO: Add authentication logic (API call, validation, etc.)

    // If login is successful, navigate to the home page
    //navigate("/");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-blue-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl w-full grid grid-cols-2 gap-4">
        <div className="pr-22">
          <img
            className="mx-auto md:w-auto w-full"
            src="https://res.cloudinary.com/dvgieawnp/image/upload/v1695989200/emancipation-abstract-concept-illustration-businessman-ambition-motivation-work-office-success_335657-639_esdima.avif"
            alt="Illustration"
          />
        </div>
        <div className="space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Sign in to your account
            </h2>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleLogin}>
            <input type="hidden" name="remember" value="true" />
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="email-address" className="">
                  Email address
                </label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                  placeholder="Email Address"
                />
              </div>
              <div>
                <label htmlFor="password" className="">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                  placeholder="Password"
                />
              </div>
            </div>
            <div>
              <button
                type="submit"
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Sign in
              </button>
              <button
                type="button"
                onClick={redirectToSignup}
                className="group relative w-full flex justify-center mt-2 py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Create new account?
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;

import { Link } from "react-router-dom";
import { ArrowLeftCircle } from "lucide-react";

const NotFound = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white px-4">
            <h1 className="text-6xl font-bold text-red-500">404</h1>
            <h2 className="text-2xl font-semibold mt-4">Page Not Found</h2>
            <p className="text-gray-400 mt-2 text-center">
                Oops! The page you're looking for doesn't exist or has been moved.
            </p>
            <Link to="/" className="mt-6 flex items-center gap-2 text-blue-400 hover:text-blue-300 transition">
                <ArrowLeftCircle className="w-5 h-5" />
                <span>Go Back Home</span>
            </Link>
        </div>
    );
};

export default NotFound;
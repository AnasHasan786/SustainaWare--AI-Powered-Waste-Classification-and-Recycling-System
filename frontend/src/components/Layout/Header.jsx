import { Link } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import { Menu, X, ChevronDown } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

const Header = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);
    const { user, logout } = useAuth();

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setDropdownOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    return (
        <header className="fixed top-0 left-0 w-full bg-white/90 backdrop-blur-lg z-50">
            <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
                
                {/* Logo */}
                <Link to="/" className="text-3xl font-bold text-gray-900 tracking-wide hover:text-gray-900 transition-all duration-300">
                    Sustaina
                    <span className="text-green-600 transition-all duration-300 hover:text-gray-900">Ware</span>
                </Link>

                {/* Mobile Menu */}
                <button onClick={() => setIsOpen(!isOpen)} className="md:hidden p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition">
                    {isOpen ? <X className="w-6 h-6 text-gray-700" /> : <Menu className="w-6 h-6 text-gray-700" />}
                </button>

                {/* Mobile Menu Content */}
                {isOpen && (
                    <div className="absolute top-16 left-0 w-full bg-white shadow-lg py-4 flex flex-col items-center md:hidden transition-all duration-300 ease-in-out">
                        {["Home", "About", "Features", "Services", "Blog", "Contact"].map((item, index) => (
                            <Link 
                                key={index}
                                to={item === "Home" ? "/" : `/${item.toLowerCase().replace(" ", "")}`}
                                className="py-2 text-gray-700 font-semibold hover:text-green-600 transition duration-300"
                                onClick={() => setIsOpen(false)}
                            >
                                {item}
                            </Link>
                        ))}
                    </div>
                )}

                {/* Authentication Section */}
                {user ? (
                    <div className="relative" ref={dropdownRef}>
                        <button onClick={() => setDropdownOpen(!dropdownOpen)} className="flex items-center gap-2 hover:text-black-600 transition-all duration-300 cursor-pointer">
                            <img src={user.photoURL || "/default-avatar.png"} alt="User" className="w-10 h-10 rounded-full border-2 border-black-500" />
                            <ChevronDown className="w-5 h-5 text-gray-700" />
                        </button>
                        {dropdownOpen && (
                            <div className="absolute right-0 mt-3 w-48 bg-white shadow-lg rounded-lg py-2 text-gray-700 border border-gray-200 animate-fade-in">
                                <p className="px-4 py-2 font-medium text-gray-900">{user.displayName}</p>
                                <Link to="/account" className="block px-4 py-2 hover:bg-gray-100 cursor-pointer">My Account</Link>
                                <button onClick={logout} className="block w-full text-left px-4 py-2 text-red-500 hover:bg-gray-100 cursor-pointer">Sign Out</button>
                            </div>
                        )}
                    </div>
                ) : (
                    <Link to="/login" className="bg-black text-white px-6 py-2 rounded-full text-sm font-semibold hover:bg-[#111111] transition duration-300 hover:scale-105">
                        Sign In
                    </Link>
                )}
            </div>
        </header>
    );
};

export default Header;

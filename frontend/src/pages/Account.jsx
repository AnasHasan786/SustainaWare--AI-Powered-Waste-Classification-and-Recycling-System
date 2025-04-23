import { useEffect, useState } from "react";
import { getFeedbacks, deleteFeedback } from "../api/feedback";
import { getUserProfile } from "../api/auth";
import FeedbackForm from "../components/Feedback/FeedbackForm";
import { Loader2, Trash2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Account = () => {
    const { user: authUser, loading: authLoading } = useAuth();
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [feedbacks, setFeedbacks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [hover, setHover] = useState(false);

    useEffect(() => {
        if (!authLoading && !authUser) {
            navigate("/login");
        }
    
        const fetchUserData = async () => {
            try {
                const userData = await getUserProfile();
                setUser(userData);
                
                const userFeedbacks = await getFeedbacks(authUser.id);  
                setFeedbacks(userFeedbacks);
            } catch (err) {
                setError("Failed to fetch user data.");
            }
            setLoading(false);
        };
    
        if (authUser) {
            fetchUserData();
        }
    }, [authUser, authLoading, navigate]);

    const handleFeedbackSubmit = (newFeedback) => {
        setFeedbacks((prevFeedbacks) => [...prevFeedbacks, newFeedback]);
    };

    const handleDeleteFeedback = async (feedbackId) => {
        try {
            await deleteFeedback(feedbackId);
            setFeedbacks(feedbacks.filter((feedback) => feedback.id !== feedbackId));
        } catch (err) {
            setError("Failed to delete feedback.");
        }
    };

    if (authLoading || loading) {
        return (
            <div className="flex justify-center items-center h-screen bg-white">
                <Loader2 className="animate-spin text-gray-600" size={40} />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-white text-gray-900 py-20 px-4 flex flex-col items-center">
            {/* User Profile Section */}
            <div className="w-full max-w-3xl flex items-center space-x-6 mb-8">
                <div
                    className="w-20 h-20 relative cursor-pointer rounded-full overflow-hidden"
                    onMouseEnter={() => setHover(true)}
                    onMouseLeave={() => setHover(false)}
                >
                    <img
                        src={user?.profilePicture ? `${user.profilePicture}?${new Date().getTime()}` : "/default-avatar.png"}
                        alt="Profile"
                        className="w-full h-full object-cover"
                    />
                </div>

                <div>
                    <h3 className="text-2xl font-bold">{user?.name}</h3>
                    <p className="text-gray-600">{user?.email}</p>
                </div>
            </div>

            {/* User Feedback Section */}
            <h3 className="text-2xl font-semibold mb-4">My Feedback</h3>
            {feedbacks.length === 0 ? (
                <p className="text-gray-500 italic">No feedback submitted yet.</p>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-3xl">
                    {feedbacks.map((feedback) => (
                        <div key={feedback.id} className="p-4 bg-gray-50 rounded-lg">
                            <p className="text-gray-700 text-lg">
                                {feedback.feedback_text ? feedback.feedback_text : <i>No text provided</i>}
                            </p>
                            <div className="flex justify-between items-center mt-4">
                                <span className="text-yellow-500 font-semibold">{feedback.rating} ⭐</span>
                                <button
                                    onClick={() => handleDeleteFeedback(feedback.id)}
                                    className="text-red-500 hover:text-red-700 transition-all duration-200 ease-in-out"
                                >
                                    <Trash2 size={20} />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Submit Feedback Section */}
            <h3 className="text-2xl font-semibold mt-8 mb-4">Submit Feedback</h3>
            <div className="w-full max-w-3xl">
                <FeedbackForm onFeedbackSubmit={handleFeedbackSubmit} />
            </div>
        </div>
    );
};

export default Account;

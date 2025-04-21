import { useState, useEffect } from "react";
import { sendFeedback } from "../../api/feedback";
import { useAuth } from "../../context/AuthContext";
import { Loader2 } from "lucide-react";
import { useNavigate } from "react-router-dom";

const FeedbackForm = ({ onFeedbackSubmit }) => {
    const { user, loading: authLoading } = useAuth();
    const [feedback, setFeedback] = useState("");
    const [rating, setRating] = useState(5);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        if (!authLoading && !user) {
            navigate("/login");
        }
    }, [authLoading, user, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!feedback.trim()) {
            setMessage("Feedback cannot be empty.");
            return;
        }

        if (!user) {
            setMessage("You must be logged in to submit feedback.");
            return;
        }

        setLoading(true);
        try {
            const newFeedback = await sendFeedback({ userId: user?.id, feedback_text: feedback, rating });
            setMessage("Thank you for your feedback!");
            setFeedback("");
            setRating(5);

            onFeedbackSubmit(newFeedback);
        } catch (error) {
            setMessage(error.response?.status === 401 ? "You must be logged in to submit feedback." : "Failed to submit feedback. Try again!");
        }
        setLoading(false);
    };

    return (
        <div className="bg-white shadow-lg rounded-xl p-8 w-full max-w-lg mx-auto border border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900 text-center mb-6">We Value Your Feedback</h2>

            {message && <p className="text-sm text-center font-medium text-red-500 mb-4">{message}</p>}

            <form onSubmit={handleSubmit} className="space-y-5">
                <textarea
                    className="w-full p-4 border border-gray-300 rounded-lg bg-gray-50 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows="4"
                    placeholder="Write your feedback here..."
                    value={feedback}
                    onChange={(e) => setFeedback(e.target.value)}
                    required
                />

                <div className="flex items-center space-x-3">
                    <span className="text-gray-700 font-medium">Rate Us:</span>
                    <input
                        type="range"
                        min="1"
                        max="5"
                        value={rating}
                        onChange={(e) => setRating(Number(e.target.value))}
                        className="cursor-pointer w-full"
                    />
                    <span className="text-lg font-semibold text-gray-900">
                        {Array.from({ length: rating }).map((_, i) => "⭐")}
                    </span>
                </div>

                <button
                    type="submit"
                    disabled={loading || authLoading}
                    className="w-full flex items-center justify-center bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-lg transition duration-300 cursor-pointer"
                >
                    {loading ? <Loader2 className="animate-spin mr-2" size={20} /> : "Submit Feedback"}
                </button>
            </form>
        </div>
    );
};

export default FeedbackForm;

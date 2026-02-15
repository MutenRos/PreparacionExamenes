'use client';

import { useState } from 'react';

interface Question {
  question: string;
  options: string[];
  correctAnswer: number;
}

interface LessonQuizProps {
  questions?: Question[];
  quiz?: any;
  lessonId?: string;
}

export function LessonQuiz({ questions, quiz, lessonId }: LessonQuizProps) {
  const quizQuestions = questions || quiz?.questions || [];
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);

  const handleAnswer = (index: number) => {
    setSelectedAnswer(index);
    setShowResult(true);
    
    if (index === quizQuestions[currentQuestion].correctAnswer) {
      setScore(score + 1);
    }

    setTimeout(() => {
      if (currentQuestion < quizQuestions.length - 1) {
        setCurrentQuestion(currentQuestion + 1);
        setSelectedAnswer(null);
        setShowResult(false);
      }
    }, 1500);
  };

  if (currentQuestion >= quizQuestions.length || quizQuestions.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-8 text-center">
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h3 className="text-2xl font-bold mb-2">¡Quiz Completado!</h3>
        <p className="text-gray-600 mb-6">
          Puntuación: {score} de {quizQuestions.length}
        </p>
        <button
          onClick={() => {
            setCurrentQuestion(0);
            setScore(0);
            setSelectedAnswer(null);
            setShowResult(false);
          }}
          className="px-6 py-3 bg-stone-600 text-white rounded-lg hover:bg-stone-700"
        >
          Reintentar
        </button>
      </div>
    );
  }

  const question = quizQuestions[currentQuestion];

  return (
    <div className="bg-white rounded-lg shadow-lg p-8">
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <span className="text-sm text-gray-500">
            Pregunta {currentQuestion + 1} de {quizQuestions.length}
          </span>
          <span className="text-sm font-medium text-stone-600">
            Puntuación: {score}
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-stone-600 h-2 rounded-full transition-all"
            style={{ width: `${((currentQuestion + 1) / quizQuestions.length) * 100}%` }}
          />
        </div>
      </div>

      <h3 className="text-xl font-bold mb-6">{question?.question || ''}</h3>

      <div className="space-y-3">
        {(question?.options || []).map((option: string, index: number) => (
          <button
            key={index}
            onClick={() => !showResult && handleAnswer(index)}
            disabled={showResult}
            className={`w-full p-4 text-left rounded-lg border-2 transition-all ${
              showResult
                ? index === question?.correctAnswer
                  ? 'border-green-500 bg-green-50'
                  : index === selectedAnswer
                  ? 'border-red-500 bg-red-50'
                  : 'border-gray-200'
                : 'border-gray-200 hover:border-stone-500 hover:bg-stone-50'
            }`}
          >
            <div className="flex items-center justify-between">
              <span>{option}</span>
              {showResult && index === question?.correctAnswer && (
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              )}
              {showResult && index === selectedAnswer && index !== question?.correctAnswer && (
                <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              )}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

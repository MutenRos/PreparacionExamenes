import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

export interface CourseMetadata {
  id: string;
  slug: string;
  title: string;
  subtitle?: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  lessons: number;
  has_project?: boolean;
  estimated_duration_hours?: number;
  tags?: string[];
}

export interface Course {
  metadata: CourseMetadata;
  content: string;
}

const COURSES_DIRECTORY = path.join(process.cwd(), 'content/courses');

export function getCourseBySlug(slug: string): Course | null {
  try {
    const fullPath = path.join(COURSES_DIRECTORY, `${slug}.md`);
    
    if (!fs.existsSync(fullPath)) {
      return null;
    }

    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const { data, content } = matter(fileContents);

    return {
      metadata: data as CourseMetadata,
      content,
    };
  } catch (error) {
    console.error(`Error reading course ${slug}:`, error);
    return null;
  }
}

export function getAllCourses(): Course[] {
  try {
    if (!fs.existsSync(COURSES_DIRECTORY)) {
      return [];
    }

    const fileNames = fs.readdirSync(COURSES_DIRECTORY);
    const courses = fileNames
      .filter(fileName => fileName.endsWith('.md'))
      .map(fileName => {
        const slug = fileName.replace(/\.md$/, '');
        return getCourseBySlug(slug);
      })
      .filter((course): course is Course => course !== null);

    return courses;
  } catch (error) {
    console.error('Error reading courses:', error);
    return [];
  }
}

export function getCoursesByCategory(category: string): Course[] {
  const allCourses = getAllCourses();
  return allCourses.filter(course => course.metadata.category === category);
}

export function getCoursesByTag(tag: string): Course[] {
  const allCourses = getAllCourses();
  return allCourses.filter(course => 
    course.metadata.tags?.includes(tag)
  );
}

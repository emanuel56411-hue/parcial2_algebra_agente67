import tutorAvatar from "@/assets/tutor-avatar.webp"
import { cn } from "@/lib/utils"

export function TutorAvatar({ className, eager = false }: { className?: string; eager?: boolean }) {
  return <img
    src={tutorAvatar}
    alt=""
    width={512}
    height={512}
    loading={eager ? "eager" : "lazy"}
    decoding="async"
    className={cn("shrink-0 rounded-full object-cover", className)}
  />
}

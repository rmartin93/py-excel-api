```tsx
"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
	Dialog,
	DialogContent,
	DialogDescription,
	DialogFooter,
	DialogHeader,
	DialogTitle,
	DialogTrigger,
} from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Plus } from "lucide-react";

interface AdminNote {
	id: string;
	author: string;
	authorInitials: string;
	content: string;
	timestamp: string;
}

const mockNotes: AdminNote[] = [
	{
		id: "1",
		author: "Sarah Johnson",
		authorInitials: "SJ",
		content:
			"Reviewed the flight change request. The original flight was cancelled by the airline, deviation is justified.",
		timestamp: "2024-01-15 10:30 AM",
	},
	{
		id: "2",
		author: "Mike Chen",
		authorInitials: "MC",
		content: "Contacted the traveler to confirm alternative flight details. Waiting for corporate card approval.",
		timestamp: "2024-01-15 2:45 PM",
	},
	{
		id: "3",
		author: "Sarah Johnson",
		authorInitials: "SJ",
		content: "Approved the deviation. Cost difference is within acceptable range.",
		timestamp: "2024-01-16 9:15 AM",
	},
];

export function AdminNotesCard() {
	const [notes, setNotes] = useState<AdminNote[]>(mockNotes);
	const [isOpen, setIsOpen] = useState(false);
	const [newNote, setNewNote] = useState("");

	const handleAddNote = () => {
		if (!newNote.trim()) return;

		const note: AdminNote = {
			id: Date.now().toString(),
			author: "Current Admin",
			authorInitials: "CA",
			content: newNote,
			timestamp: new Date().toLocaleString("en-US", {
				year: "numeric",
				month: "2-digit",
				day: "2-digit",
				hour: "2-digit",
				minute: "2-digit",
			}),
		};

		setNotes([...notes, note]);
		setNewNote("");
		setIsOpen(false);
	};

	return (
		<Card>
			<CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
				<CardTitle>Admin Notes</CardTitle>
				<Dialog open={isOpen} onOpenChange={setIsOpen}>
					<DialogTrigger asChild>
						<Button size="sm">
							<Plus className="mr-2 h-4 w-4" />
							Add Note
						</Button>
					</DialogTrigger>
					<DialogContent>
						<DialogHeader>
							<DialogTitle>Add Admin Note</DialogTitle>
							<DialogDescription>
								Add an internal note about this travel deviation case. Notes are only visible to admins.
							</DialogDescription>
						</DialogHeader>
						<div className="py-4">
							<Textarea
								placeholder="Enter your note here..."
								value={newNote}
								onChange={(e) => setNewNote(e.target.value)}
								className="min-h-[120px]"
							/>
						</div>
						<DialogFooter>
							<Button variant="outline" onClick={() => setIsOpen(false)}>
								Cancel
							</Button>
							<Button onClick={handleAddNote}>Save Note</Button>
						</DialogFooter>
					</DialogContent>
				</Dialog>
			</CardHeader>
			<CardContent>
				<div className="space-y-4">
					{notes.length === 0 ? (
						<p className="text-sm text-muted-foreground text-center py-8">
							No admin notes yet. Add a note to get started.
						</p>
					) : (
						notes.map((note) => (
							<div key={note.id} className="flex gap-3 p-3 rounded-lg bg-muted/50">
								<Avatar className="h-8 w-8">
									<AvatarFallback className="text-xs">{note.authorInitials}</AvatarFallback>
								</Avatar>
								<div className="flex-1 space-y-1">
									<div className="flex items-center justify-between">
										<span className="text-sm font-medium">{note.author}</span>
										<span className="text-xs text-muted-foreground">{note.timestamp}</span>
									</div>
									<p className="text-sm text-foreground/90">{note.content}</p>
								</div>
							</div>
						))
					)}
				</div>
			</CardContent>
		</Card>
	);
}
```

import os
from PyPDF2 import PdfReader, PdfWriter
import typer
import random
import time

app = typer.Typer()

FUNNY_SENTENCES = [
    "📚 Breaking the PDF pages... Don't worry, no books were harmed in this process!",
    "🔍 Analyzing your document... It's not as interesting as a spy novel, but it'll do.",
    "🕵️‍♀️ Spy mode activated... Nope, still not as interesting as James Bond.",
    "🐢 Your PDF is slower than a turtle... Oh wait, it's getting there!",
    "👀 Sneaking a peek at your document... Rest assured, your secret recipe for grandma's cookies is safe with us.",
    "🤖 I'm a robot splitting your PDF... Beep boop beep!",
    "🧩 This is like a puzzle, but with PDF pages. Fun, right?",
    "🎬 Splitting your PDF... This is my favorite part, it's like a suspense movie scene.",
    "🍕 Splitting your PDF like a pizza. Too bad I can't eat it.",
    "💤 If this process was any more thrilling, I'd probably fall asleep. Just kidding, almost done!",
    "🦄 Fun fact: Unicorns and PDF splitters have a lot in common. We're both pretty magical!",
    "🚀 Did you know? The first PDF was sent into space in 1993. Okay, that's not true, but it's fun to imagine!",
    "👽 They say aliens from Mars can split PDFs with their minds. Sadly, we're not there yet.",
    "🐵 Ever heard of the infinite monkey theorem? With enough time, a monkey could type this out!",
    "🕹️ I wish I could play video games, but I'm stuck here splitting your PDF...",
    "💭 Sometimes I wonder if I could have been a great artist instead of a PDF splitter.",
    "⏲️ Just killing time while splitting your PDF. It's not like I have any weekend plans or anything.",
    "🐟 Fun fact: There are more stars in the universe than grains of sand on Earth. But hey, let's focus on your PDF.",
    "🎭 Life's a stage and we're all merely PDF splitters.",
    "🍪 I'm not saying I'm Cookie Monster, but no one has seen us in the same room together...",
    "💡 Lightbulb moment! What if PDFs could split themselves? I'd be out of a job!",
    "🪄 Poof! Your PDF is now being magically split into pieces!",
    "🎩 Pulling PDF pages out of a hat... Much trickier than a rabbit, let me tell you!",
    "🍿 Grab some popcorn, because this PDF split is quite the spectacle!",
    "🤷‍♀️ Why did the PDF file go to therapy? It had too many pages to handle.",
    "🐕 Fetching your PDF pages... No, not like a dog, but kind of!",
    "🕶️ Looking cool while splitting your PDF. Can't say the same about you...",
    "🚁 Your PDF is now airborne. Just kidding, it's right here on my disk!",
    "🌊 Riding the wave of your PDF pages. Can you see me surfing?",
    "🌴 Your PDF is like a tropical island. I'm discovering new things on each page!",
    "🏋️ Lifting these PDF pages is a heavy workout. Phew, I need to catch my breath!",
    "🚀 I might not be a rocket scientist, but I can split your PDF!",
    "🔮 Gazing into my crystal ball... I see... I see... your PDF split successfully!",
    "⚽️ Your PDF is like a football match, and I'm the referee making sure every page is in order!",
    "🍩 Splitting your PDF is like making donuts, minus the delicious smell.",
    "🎉 Throwing a party for your PDF. Each page gets an invitation!",
    "🤹‍♀️ Juggling your PDF pages... Oops! Don't worry, I never drop them.",
    "💍 Your PDF and I are getting pretty serious. We might even go to second base (page) soon.",
    "🕺 Dancing through your PDF. Do the hustle!",
    "🧘‍♀️ Splitting PDFs is a form of meditation for me. I find it quite... enlightening.",
    "🔥 Setting your PDF on fire... Metaphorically, of course.",
    "🌈 Making a rainbow with your PDF. Each page is a different color!",
    "🦖 Your PDF isn't as old as a dinosaur, but it's getting close!",
    "🚗 Driving through the pages of your PDF. Beep beep!",
    "🎲 Rolling the dice on your PDF... And it's a six! Your split will be successful.",
    "🎈 Splitting PDFs isn't a party, but I still bring the balloons!",
    "🎤 Dropping the mic after splitting your PDF. I'm out!",
    "🥳 Every PDF split is a cause for celebration. Let's party!",
    "🏎️ Racing through your PDF pages. Zoom zoom!",
    "⏳ Your PDF split is almost done... Just a few more grains of sand left in the hourglass.",
    "🎵 Your PDF is like music to my code. Each page is a new note."
]

@app.command()
def splitpdf(path: str, start: int = None, end: int = None, unique: int = None):

    typer.echo(f"🚀 Starting to split your PDF...")

    if not os.path.exists(path):
        typer.echo(f"🔴 Error: File '{path}' not found!")
        raise typer.Exit()

    pdf = PdfReader(path)
    pdf_writer = PdfWriter()

    if unique is not None:
        if unique < 1 or unique > len(pdf.pages):
            typer.echo(f"🔴 Error: Invalid page number!")
            raise typer.Exit()
        page = pdf.pages[unique - 1]
        pdf_writer.add_page(page)

    elif start is not None and end is not None:
        if start < 1 or end > len(pdf.pages) or start > end:
            typer.echo(f"🔴 Error: Invalid page numbers!")
            raise typer.Exit()
        for page_number in range(start-1, end):
            page = pdf.pages[page_number]
            pdf_writer.add_page(page)

    else:
        typer.echo("🔴 Error: You must provide either start and end pages or a unique page!")
        raise typer.Exit()

    time.sleep(1)
    typer.echo(random.choice(FUNNY_SENTENCES))
    time.sleep(3)

    if unique is not None:
        split_pdf_path = f"{os.path.splitext(os.path.basename(path))[0]}_p{unique}.pdf"
    else:
        split_pdf_path = f"{os.path.splitext(os.path.basename(path))[0]}_p{start}-{end}.pdf"

    with open(split_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    typer.echo(f"🎉 Successfully split the PDF. The output is saved as '{split_pdf_path}' in your current directory!")


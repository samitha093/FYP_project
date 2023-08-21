package com.example.predictionapp;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.WindowDecorActionBar;
import androidx.recyclerview.widget.RecyclerView;

import com.squareup.picasso.Picasso;

import java.util.List;

public class ProductAdapter extends RecyclerView.Adapter<ProductAdapter.ViewHolder> {

    private List<String> imageUrlList;
    private List<Product> productList;


    public ProductAdapter(List<Product> productList) {
        this.productList = productList;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.tile_item, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
       /* String imageUrl = imageUrlList.get(position);
        // Load and display the image using a library like Picasso or Glide
        Picasso.get().load(imageUrl).into(holder.imgProduct);*/
        Product product = productList.get(position);

        // Load and display the image using Picasso or Glide
        Picasso.get().load(product.getImageUrl()).into(holder.imgProduct);

        // Set the product name and price
        holder.tvItemName.setText(product.getItemName());
        holder.tvItemPrice.setText(product.getItemPrice());
    }

    @Override
    public int getItemCount() {
        return productList.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {

        ImageView imgProduct;
        private TextView tvItemName, tvItemPrice;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            imgProduct = itemView.findViewById(R.id.imgProduct);
            tvItemName = itemView.findViewById(R.id.tvItemName);
            tvItemPrice= itemView.findViewById(R.id.tvItemPrice);
        }
    }
}
